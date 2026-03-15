/**
 * UI Application State Store
 * Manages purely client-side UI state (modals, navigation, selections).
 * Does NOT hold server data (that's in apiStore).
 */
import { $state } from 'svelte/state';

export const uiStore = $state({
  // Navigation
  currentRoute: '/',
  sidebarOpen: false,

  // Modal states
  createHeroineModalOpen: false,
  refineNPCModalOpen: false,
  branchModalOpen: false,
  diffViewerOpen: false,

  // Selection state
  selectedBeadId: null as string | null,
  selectedNPCId: null as string | null,
  selectedSceneId: null as string | null,
  currentBranch: 'main',

  // Transient UI state
  isLoading: false,
  errorMessage: null as string | null,
  toast: null as { message: string; type: 'success' | 'error' | 'info' } | null,

  // Editor state
  editorMode: 'view' as 'view' | 'edit' | 'refine',

  // Phaser canvas state
  canvasScale: 1,
  showNebula: true,
  showLabels: true
});

/**
 * Show a toast notification
 */
export function showToast(message: string, type: 'success' | 'error' | 'info' = 'info'): void {
  uiStore.toast = { message, type };
  setTimeout(() => {
    uiStore.toast = null;
  }, 3000);
}

/**
 * Set loading state with optional error
 */
export function setLoading(isLoading: boolean, error?: string): void {
  uiStore.isLoading = isLoading;
  if (error) {
    uiStore.errorMessage = error;
  }
}
