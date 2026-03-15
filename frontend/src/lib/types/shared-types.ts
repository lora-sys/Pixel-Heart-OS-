/**
 * Shared type definitions between frontend and backend.
 * These types mirror the backend Pydantic schemas.
 *
 * In production, these could be auto-generated from the OpenAPI spec.
 */

// === Beads ===
export interface Bead {
  id: string;
  parent_id: string | null;
  branch_name: string;
  timestamp: string;
  action: string;
  emotion_tag?: string;
  content: Record<string, any>;
  signature?: string;
}

export interface BeadSummary {
  id: string;
  parent_id: string | null;
  branch_name: string;
  timestamp: string;
  action: string;
  emotion_tag?: string;
  content_preview?: string;
}

// === Heroine ===
export interface SoulStructure {
  core_traumas: Array<{ event: string; emotional_impact: string }>;
  defense_mechanisms: string[];
  ideal_type: {
    attraction_traits: string[];
    aversion_traits: string[];
  };
  scene_preferences: string[];
}

export interface Identity {
  name: string;
  age: number;
  appearance: string;
  personality: string;
  backstory: string;
}

export interface VoiceConfig {
  speech_patterns: Record<string, any>;
  vocabulary: Record<string, any>;
  emotional_tone: Record<string, string>;
}

export interface Heroine {
  id: string;
  soul: SoulStructure;
  identity: Identity;
  voice: VoiceConfig;
  created_at: string;
}

// === NPC ===
export interface NPC {
  id: string;
  name: string;
  role: 'protector' | 'competitor' | 'shadow';
  soul: Record<string, any>;
  identity: Record<string, any>;
  voice: Record<string, any>;
  created_at: string;
  relationship_to_heroine?: string;
}

// === Scene ===
export interface Scene {
  id: string;
  name: string;
  description: string;
  config: Record<string, any>;
  image_path?: string;
  created_at: string;
}

// === Relationship Nebula (for Phaser visualization) ===
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

// === API Request/Response ===
export interface ApiResponse<T> {
  data: T;
  error?: string;
  timestamp: string;
}

// === Simulation ===
export interface SimulationState {
  current_scene: Scene | null;
  active_npcs: NPC[];
  relationships: Record<string, number>; // npc_id -> trust_score
  current_bead_id: string | null;
  available_branches: string[];
}

export interface SimulationTurnResult {
  bead_id: string;
  responses: Array<{
    npc_id: string;
    npc_name: string;
    dialogue: string;
    emotion: string;
    relationship_delta: number;
  }>;
  updated_relationships: Record<string, number>;
  next_beads: string[];
  branch_name: string;
  timestamp: string;
}
