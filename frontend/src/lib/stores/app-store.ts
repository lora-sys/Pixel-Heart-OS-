/**
 * Global application state using Svelte 5 Runes ($state)
 */
export interface Heroine {
  id: string;
  soul: {
    core_traumas: Array<{ event: string; emotional_impact: string }>;
    defense_mechanisms: string[];
    ideal_type: {
      attraction_traits: string[];
      aversion_traits: string[];
    };
    scene_preferences: string[];
  };
  identity: {
    name: string;
    age: number;
    appearance: string;
    personality: string;
    backstory: string;
  };
  voice: Record<string, any>;
  created_at: string;
}

export interface NPC {
  id: string;
  name: string;
  role: 'protector' | 'competitor' | 'shadow';
  soul: Record<string, any>;
  identity: Record<string, any>;
  voice: Record<string, any>;
  created_at: string;
}

export interface Scene {
  id: string;
  name: string;
  description: string;
  config: Record<string, any>;
  image_path?: string;
  created_at: string;
}

export interface Bead {
  id: string;
  parent_id: string | null;
  branch_name: string;
  timestamp: string;
  action: string;
  emotion_tag?: string;
  content: Record<string, any>;
}

export interface NebulaNode {
  id: string;
  label: string;
  type: 'heroine' | 'npc';
  x: number;
  y: number;
  color: string;
  size: number;
}

export interface NebulaEdge {
  source: string;
  target: string;
  strength: number;
  type: 'protector' | 'competitor' | 'shadow' | 'neutral';
}

export interface AppState {
  heroine: Heroine | null;
  npcs: NPC[];
  currentScene: Scene | null;
  beads: Bead[];
  currentBranch: string;
  relationshipNebula: {
    nodes: NebulaNode[];
    edges: NebulaEdge[];
  };
  activeNPCs: NPC[]; // NPCs present in current scene
}

export const state = $state<AppState>({
  heroine: null,
  npcs: [],
  currentScene: null,
  beads: [],
  currentBranch: 'main',
  relationshipNebula: { nodes: [], edges: [] },
  activeNPCs: []
});

// Derived stores (computed)
export const calculatedNPCs = $derived(() => {
  return state.npcs;
});

export const timelineBranches = $derived(() => {
  // Extract unique branch names from beads
  const branches = new Set(state.beads.map(b => b.branch_name));
  return Array.from(branches);
});

export const currentBead = $derived(() => {
  if (state.beads.length === 0) return null;
  return state.beads[state.beads.length - 1]; // last bead is HEAD
});
