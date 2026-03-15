/**
 * Simulation Service - API client for simulation endpoints
 */
import { dedupedFetch } from '../api/client';

export interface SimulationTurnRequest {
  player_action: string;
  bead_id?: string;
}

export interface SimulationTurnResponse {
  bead_id: string;
  responses: Array<{ npc_id: string; dialogue: string; emotion: string; relationship_delta: number }>;
  updated_relationships: Record<string, number>;
  next_beads: string[];
}

export interface SimulationStateResponse {
  current_scene: any; // TODO: use Scene type
  active_npcs: Array<any>; // TODO: use NPC type
  relationships: Record<string, number>;
  current_bead_id: string | null;
  available_branches: string[];
}

class SimulationService {
  private basePath = '/api/v1/simulate';

  async getState(): Promise<SimulationStateResponse> {
    return dedupedFetch<SimulationStateResponse>(`${this.basePath}/state`, {
      cacheKey: 'simulation:state',
      cacheTtl: 30000 // 30 seconds (frequent updates)
    });
  }

  async takeTurn(request: SimulationTurnRequest): Promise<SimulationTurnResponse> {
    return dedupedFetch<SimulationTurnResponse>(`${this.basePath}/turn`, {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }
}

export const simulationService = new SimulationService();
