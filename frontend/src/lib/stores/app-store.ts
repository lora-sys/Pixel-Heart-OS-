/**
 * DEPRECATED: Use core/store/app-store.ts for UI state and core/store/api-store.ts for server state.
 *
 * This file is kept for backward compatibility during migration.
 * New code should import from:
 *   import { uiStore, apiStore } from '$lib/core/store';
 */

// Re-export from new locations for backward compatibility
export { uiStore, showToast, setLoading } from '../core/store/app-store';
export { apiStore, cacheData, getCachedData, invalidateCache, clearCache, API_CACHE_KEYS } from '../core/store/api-store';

// Legacy types (moved to shared-types.ts)
// TODO: migrate imports to use shared-types.ts directly
export type { Heroine, NPC, Scene, Bead, NebulaNode, NebulaEdge, AppState } from '../types/shared-types';

// Legacy derived stores (moved to derived stores)
export const calculatedNPCs = $derived(() => apiStore.npcs);
export const timelineBranches = $derived(() => {
  const branches = new Set(apiStore.beads.map(b => b.branch_name));
  return Array.from(branches);
});
export const currentBead = $derived(() => {
  if (apiStore.beads.length === 0) return null;
  return apiStore.beads[apiStore.beads.length - 1];
});
