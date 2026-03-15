/**
 * NPC Service - API client for NPC endpoints
 */
import { dedupedFetch } from '../api/client';
import type { NPC } from '../types/shared-types';

export interface NPCResponse {
  id: string;
  name: string;
  role: string;
  relationship_to_heroine: string;
  soul: Record<string, any>;
  identity: Record<string, any>;
  voice: Record<string, any>;
  created_at: string;
}

export interface NPCRefineRequest {
  feedback: string;
}

export interface NPCRefineResponse {
  original: Record<string, any>;
  suggested: Record<string, any>;
  diff: Array<{ field: string; from: any; to: any }>;
}

class NPCService {
  private basePath = '/api/v1/npcs';

  async generate(): Promise<NPCResponse[]> {
    return dedupedFetch<NPCResponse[]>(`${this.basePath}/generate`, {
      method: 'POST'
    });
  }

  async list(): Promise<NPCResponse[]> {
    return dedupedFetch<NPCResponse[]>(`${this.basePath}/`, {
      cacheKey: 'npcs:list',
      cacheTtl: 120000 // 2 minutes
    });
  }

  async get(id: string): Promise<NPCResponse> {
    return dedupedFetch<NPCResponse>(`${this.basePath}/${id}`, {
      cacheKey: `npc:${id}`,
      cacheTtl: 120000
    });
  }

  async refine(id: string, feedback: string): Promise<NPCRefineResponse> {
    return dedupedFetch<NPCRefineResponse>(`${this.basePath}/${id}/refine`, {
      method: 'PATCH',
      body: JSON.stringify({ feedback })
    });
  }

  async applyRefinement(id: string, refinedData: Record<string, any>): Promise<{ status: string; npc_id: string }> {
    return dedupedFetch(`/${this.basePath}/${id}/refine/apply`, {
      method: 'POST',
      body: JSON.stringify(refinedData)
    });
  }
}

export const npcService = new NPCService();
