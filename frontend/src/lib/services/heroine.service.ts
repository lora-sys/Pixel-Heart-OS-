/**
 * Heroine Service - API client for heroine endpoints
 */
import { dedupedFetch } from './api/client';
import type { Heroine } from '../types/shared-types';

export interface CreateHeroineRequest {
  description: string;
  input_mode: 'free_description' | 'questionnaire' | 'reality_import';
}

export interface HeroineResponse {
  id: string;
  soul: any;
  identity: any;
  voice: any;
  created_at: string;
}

class HeroineService {
  private basePath = '/api/v1/heroine';

  async create(request: CreateHeroineRequest): Promise<HeroineResponse> {
    return dedupedFetch<HeroineResponse>(`${this.basePath}/create`, {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  async get(): Promise<HeroineResponse | null> {
    return dedupedFetch<HeroineResponse | null>(`${this.basePath}/`, {
      cacheKey: 'heroine:current',
      cacheTtl: 120000 // 2 minutes
    });
  }

  async update(id: string, updates: Partial<Heroine>): Promise<HeroineResponse> {
    // PATCH endpoint would need to be added on backend
    throw new Error('Not implemented');
  }

  async refine(id: string, feedback: string): Promise<HeroineResponse> {
    // Refinement endpoint would need to be added
    throw new Error('Not implemented');
  }
}

export const heroineService = new HeroineService();
