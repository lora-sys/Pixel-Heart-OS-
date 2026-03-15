/**
 * UI Application State Store
 * Manages purely client-side UI state (modals, navigation, selections).
 * Does NOT hold server data (that's in apiStore).
 */
import { writable, type Writable } from 'svelte/store';

export const uiStore: Writable<{
  // Navigation
  currentRoute: string;
  sidebarOpen: boolean;

  // Modal states
  createHeroineModalOpen: boolean;
  refineNPCModalOpen: boolean;
  branchModalOpen: boolean;
  diffViewerOpen: boolean;

  // Selection state
  selectedBeadId: string | null;
  selectedNPCId: string | null;
  selectedSceneId: string | null;
  currentBranch: string;

  // Transient UI state
  isLoading: boolean;
  errorMessage: string | null;
  toast: { message: string; type: 'success' | 'error' | 'info' } | null;

  // Editor state
  editorMode: 'view' | 'edit' | 'refine';

  // Phaser canvas state
  canvasScale: number;
  showNebula: boolean;
  showLabels: boolean;
}> = writable({
  // Navigation
  currentRoute: '/',
  sidebarOpen: false,

  // Modal states
  createHeroineModalOpen: false,
  refineNPCModalOpen: false,
  branchModalOpen: false,
  diffViewerOpen: false,

  // Selection state
  selectedBeadId: null,
  selectedNPCId: null,
  selectedSceneId: null,
  currentBranch: 'main',

  // Transient UI state
  isLoading: false,
  errorMessage: null,
  toast: null,

  // Editor state
  editorMode: 'view',

  // Phaser canvas state
  canvasScale: 1,
  showNebula: true,
  showLabels: true
});

/**
 * Show a toast notification
 */
export function showToast(message: string, type: 'success' | 'error' | 'info' = 'info'): void {
  uiStore.update(state => ({ ...state, toast: { message, type } }));
  setTimeout(() => {
    uiStore.update(state => ({ ...state, toast: null }));
  }, 3000);
}

/**
 * Set loading state with optional error
 */
export function setLoading(isLoading: boolean, error?: string): void {
  uiStore.update(state => ({
    ...state,
    isLoading,
    errorMessage: error || null
  }));
}
