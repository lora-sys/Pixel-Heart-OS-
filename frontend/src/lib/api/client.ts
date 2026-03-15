/**
 * API client - wrappers for all backend endpoints
 */
import { apiCache } from '../cache/api-cache';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// In-flight request tracker for deduplication
const inFlightRequests = new Map<string, Promise<any>>();

async function fetchJSON<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

/**
 * Smart fetch with deduplication and caching.
 * - GET requests are cached by cacheKey (or URL if not specified)
 * - Concurrent identical requests share a single network call
 * - Cache TTL can be specified per-call or use default
 */
export async function dedupedFetch<T>(
  endpoint: string,
  options: {
    method?: string;
    body?: any;
    cacheKey?: string;
    cacheTtl?: number; // milliseconds
  } = {}
): Promise<T> {
  const method = options.method || 'GET';
  const isCacheable = method === 'GET' || method === '';

  // Build cache key
  const cacheKey = options.cacheKey ||
    (isCacheable ? `${method}${endpoint}${JSON.stringify(options.body || {})}` : null);

  // Check cache first for cacheable requests
  if (isCacheable && cacheKey) {
    const cached = apiCache.get<T>(cacheKey);
    if (cached !== null) {
      return cached;
    }
  }

  // Build deduplication key (same for all requests with same endpoint+method+body)
  const dedupKey = `${method}${endpoint}${JSON.stringify(options.body || {})}`;

  // If request already in-flight, return the same promise
  if (inFlightRequests.has(dedupKey)) {
    return inFlightRequests.get(dedupKey)!;
  }

  // Create new request promise
  const requestPromise = fetchJSON<T>(endpoint, options)
    .finally(() => {
      // Clean up in-flight tracker when done
      inFlightRequests.delete(dedupKey);
    });

  // Store in in-flight map
  inFlightRequests.set(dedupKey, requestPromise);

  try {
    const result = await requestPromise;

    // Cache successful GET responses
    if (isCacheable && cacheKey) {
      apiCache.set(cacheKey, result, options.cacheTtl);
    }

    return result;
  } catch (error) {
    // Remove from in-flight on error too
    inFlightRequests.delete(dedupKey);
    throw error;
  }
}

// === Heroine API ===
export const heroineAPI = {
  create: (description: string, mode: string = 'free_description') =>
    dedupedFetch<{ id: string; soul: any; identity: any; voice: any; created_at: string }>('/heroine/create', {
      method: 'POST',
      body: JSON.stringify({ description, input_mode: mode })
    }),

  get: () => dedupedFetch<{ id: string; soul: any; identity: any; voice: any; created_at: string } | null>('/heroine/')
};

// === NPC API ===
export const npcAPI = {
  generate: () => dedupedFetch<any[]>('/npcs/generate', { method: 'POST' }),
  list: () => dedupedFetch<any[]>('/npcs/', { cacheKey: 'npcs:list', cacheTtl: 120000 }),
  get: (id: string) => dedupedFetch<any>(`/npcs/${id}`, { cacheKey: `npc:${id}`, cacheTtl: 120000 }),
  refine: (id: string, feedback: string) =>
    dedupedFetch<{ original: any; suggested: any; diff: any[] }>(`/npcs/${id}/refine`, {
      method: 'PATCH',
      body: JSON.stringify({ feedback })
    }),
  applyRefinement: (id: string, refinedData: any) =>
    dedupedFetch<{ status: string; npc_id: string }>(`/npcs/${id}/refine/apply`, {
      method: 'POST',
      body: JSON.stringify(refinedData)
    })
};

// === Scene API ===
export const sceneAPI = {
  generate: () => dedupedFetch<any[]>('/scenes/generate', { method: 'POST' }),
  list: () => dedupedFetch<any[]>('/scenes/', { cacheKey: 'scenes:list', cacheTtl: 120000 }),
  get: (id: string) => dedupedFetch<any>(`/scenes/${id}`, { cacheKey: `scene:${id}`, cacheTtl: 120000 })
};

// === Beads API ===
export const beadsAPI = {
  getTimeline: (branch?: string) =>
    dedupedFetch<any[]>(`/beads/timeline${branch ? `?branch=${branch}` : ''}`, {
      cacheKey: `beads:timeline:${branch || 'main'}:100:0`,
      cacheTtl: 60000
    }),

  create: (data: {
    parent_id?: string;
    branch_name: string;
    action: string;
    emotion_tag?: string;
    content: Record<string, any>;
  }) =>
    dedupedFetch<any>('/beads', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  createBranch: (branchName: string, fromBeadId: string) =>
    dedupedFetch<{ branch_name: string; head_bead_id: string; message: string }>('/beads/branch', {
      method: 'POST',
      body: JSON.stringify({ branch_name: branchName, from_bead_id: fromBeadId })
    }),

  mergeBranches: (source: string, target: string, strategy?: string) =>
    dedupedFetch<any>('/beads/merge', {
      method: 'POST',
      body: JSON.stringify({ source_branch: source, target_branch: target, strategy })
    }),

  listBranches: () => dedupedFetch<{ branches: any[] }>('/beads/branches', { cacheKey: 'branches:all', cacheTtl: 120000 }),

  diff: (beadId1: string, beadId2: string) =>
    dedupedFetch<{ bead_id_earlier: string; bead_id_later: string; changes: any[] }>(
      `/beads/diff/${beadId1}/${beadId2}`
    )
};

// === Simulation API ===
export const simulationAPI = {
  getState: () =>
    dedupedFetch<{
      current_scene: any;
      active_npcs: any[];
      relationships: Record<string, number>;
      current_bead_id: string | null;
      available_branches: string[];
    }>('/simulate/state', { cacheKey: 'simulation:state', cacheTtl: 30000 }),

  takeTurn: (playerAction: string, beadId?: string) =>
    dedupedFetch<{
      bead_id: string;
      responses: Array<{ npc_id: string; dialogue: string; emotion: string; relationship_delta: number }>;
      updated_relationships: Record<string, number>;
      next_beads: string[];
    }>('/simulate/turn', {
      method: 'POST',
      body: JSON.stringify({ player_action: playerAction, bead_id: beadId })
    })
};
