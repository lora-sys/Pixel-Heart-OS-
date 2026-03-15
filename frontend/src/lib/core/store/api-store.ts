/**
 * API State Store
 * Manages cached server data (heroine, npcs, beads, scenes).
 * This store ONLY holds server state, not UI state.
 */
import { writable, type Writable } from 'svelte/store';
import type { Heroine, NPC, Bead, Scene } from '../types/shared-types';
import { apiCache } from '../../cache/api-cache';

export const API_CACHE_KEYS = {
  HEROINE: 'heroine:',
  NPC: 'npc:',
  NPC_LIST: 'npcs:list',
  BEADS_TIMELINE: (branch: string, limit: number, offset: number) =>
    `beads:timeline:${branch}:${limit}:${offset}`,
  SIMULATION_STATE: 'simulation:state',
  SCENES_LIST: 'scenes:list'
};

// Svelte 5 stores using writable (compatible with SSR)
export const apiStore: Writable<{
  heroine: Heroine | null;
  npcs: NPC[];
  beads: Bead[];
  scenes: Scene[];
  relationshipNebula: { nodes: any[]; edges: any[] };
  lastUpdated: string | null;
}> = writable({
  heroine: null,
  npcs: [],
  beads: [],
  scenes: [],
  relationshipNebula: { nodes: [], edges: [] },
  lastUpdated: null
});

// Convenience functions
export function setHeroine(heroine: Heroine | null) {
  apiStore.update(state => ({ ...state, heroine, lastUpdated: new Date().toISOString() }));
}

export function setNPCs(npcs: NPC[]) {
  apiStore.update(state => ({ ...state, npcs, lastUpdated: new Date().toISOString() }));
}

export function setBeads(beads: Bead[]) {
  apiStore.update(state => ({ ...state, beads, lastUpdated: new Date().toISOString() }));
}

export function setNebula(nodes: any[], edges: any[]) {
  apiStore.update(state => ({ ...state, relationshipNebula: { nodes, edges } }));
}

export function clearStore() {
  apiStore.set({
    heroine: null,
    npcs: [],
    beads: [],
    scenes: [],
    relationshipNebula: { nodes: [], edges: [] },
    lastUpdated: null
  });
}
