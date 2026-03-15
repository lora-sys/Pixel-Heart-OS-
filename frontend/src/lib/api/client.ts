/**
 * API client - wrappers for all backend endpoints
 */
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

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

// === Heroine API ===
export const heroineAPI = {
  create: (description: string, mode: string = 'free_description') =>
    fetchJSON<{ id: string; soul: any; identity: any; voice: any; created_at: string }>('/heroine/create', {
      method: 'POST',
      body: JSON.stringify({ description, input_mode: mode })
    }),

  get: () => fetchJSON<{ id: string; soul: any; identity: any; voice: any; created_at: string } | null>('/heroine/')
};

// === NPC API ===
export const npcAPI = {
  generate: () => fetchJSON<any[]>('/npcs/generate'),
  list: () => fetchJSON<any[]>('/npcs'),
  get: (id: string) => fetchJSON<any>(`/npcs/${id}`),
  refine: (id: string, feedback: string) =>
    fetchJSON<{ original: any; suggested: any; diff: any[] }>(`/npcs/${id}/refine`, {
      method: 'PATCH',
      body: JSON.stringify({ feedback })
    }),
  applyRefinement: (id: string, refinedData: any) =>
    fetchJSON<{ status: string; npc_id: string }>(`/npcs/${id}/refine/apply`, {
      method: 'POST',
      body: JSON.stringify(refinedData)
    })
};

// === Scene API ===
export const sceneAPI = {
  generate: () => fetchJSON<any[]>('/scenes/generate'),
  list: () => fetchJSON<any[]>('/scenes'),
  get: (id: string) => fetchJSON<any>(`/scenes/${id}`)
};

// === Beads API ===
export const beadsAPI = {
  getTimeline: (branch?: string) =>
    fetchJSON<any[]>(`/beads/timeline${branch ? `?branch=${branch}` : ''}`),

  create: (data: {
    parent_id?: string;
    branch_name: string;
    action: string;
    emotion_tag?: string;
    content: Record<string, any>;
  }) =>
    fetchJSON<any>('/beads', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  createBranch: (branchName: string, fromBeadId: string) =>
    fetchJSON<{ branch_name: string; head_bead_id: string; message: string }>('/beads/branch', {
      method: 'POST',
      body: JSON.stringify({ branch_name: branchName, from_bead_id: fromBeadId })
    }),

  mergeBranches: (source: string, target: string, strategy?: string) =>
    fetchJSON<any>('/beads/merge', {
      method: 'POST',
      body: JSON.stringify({ source_branch: source, target_branch: target, strategy })
    }),

  listBranches: () => fetchJSON<{ branches: any[] }>('/beads/branches'),

  diff: (beadId1: string, beadId2: string) =>
    fetchJSON<{ bead_id_earlier: string; bead_id_later: string; changes: any[] }>(
      `/beads/diff/${beadId1}/${beadId2}`
    )
};

// === Simulation API ===
export const simulationAPI = {
  getState: () =>
    fetchJSON<{
      current_scene: any;
      active_npcs: any[];
      relationships: Record<string, number>;
      current_bead_id: string | null;
      available_branches: string[];
    }>('/simulate/state'),

  takeTurn: (playerAction: string, beadId?: string) =>
    fetchJSON<{
      bead_id: string;
      responses: Array<{ npc_id: string; dialogue: string; emotion: string }>;
      updated_relationships: Record<string, number>;
      next_beads: string[];
    }>('/simulate/turn', {
      method: 'POST',
      body: JSON.stringify({ player_action: playerAction, bead_id: beadId })
    })
};
