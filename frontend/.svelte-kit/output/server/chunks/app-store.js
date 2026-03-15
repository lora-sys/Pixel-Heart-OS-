import { w as writable } from "./index.js";
const uiStore = writable({
  // Navigation
  currentRoute: "/",
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
  currentBranch: "main",
  // Transient UI state
  isLoading: false,
  errorMessage: null,
  toast: null,
  // Editor state
  editorMode: "view",
  // Phaser canvas state
  canvasScale: 1,
  showNebula: true,
  showLabels: true
});
export {
  uiStore as u
};
