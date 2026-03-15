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

// Note: Legacy derived stores are no longer automatically updated.
// Use $apiStore directly in components or create local derived values.
