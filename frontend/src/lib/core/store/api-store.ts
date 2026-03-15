/**
 * API State Store
 * Manages cached server data (heroine, npcs, beads, scenes).
 * This store ONLY holds server state, not UI state.
 */
import { $state } from 'svelte/state';
import type { Heroine, NPC, Bead, Scene } from '../types/shared-types';
import { apiCache } from '../../cache/api-cache';

export const API_CACHE_KEYS = {
  HEROINE: 'heroine:',
  NPC: 'npc:',
  NPC_LIST: 'npcs:list',
  BEADS_TIMELINE: (branch: string, limit: number, offset: number) =>
    `beads:timeline:${branch}:${limit}:${offset}`,
  BEAD: (id: string) => `bead:${id}`,
  SCENE: (id: string) => `scene:${id}`,
  SIMULATION_STATE: 'simulation:state',
  BRANCHES: 'branches:all'
} as const;

export const apiStore = $state({
  // Cached server data
  heroine: null as Heroine | null,
  npcs: [] as NPC[],
  beads: [] as Bead[],
  scenes: [] as Scene[],
  simulationState: null as any,

  // Metadata
  lastUpdated: null as string | null,
  loading: false,
  error: null as string | null
});

/**
 * Helper: Cache data with TTL
 */
export function cacheData<T>(key: string, data: T, ttlMs?: number): void {
  apiCache.set(key, data, ttlMs);
}

/**
 * Helper: Get cached data
 */
export function getCachedData<T>(key: string): T | null {
  return apiCache.get<T>(key);
}

/**
 * Invalidate cache for a specific key pattern
 */
export function invalidateCache(pattern: string): void {
  apiCache.invalidatePattern(pattern);
}

/**
 * Clear all cache
 */
export function clearCache(): void {
  apiCache.clear();
}
