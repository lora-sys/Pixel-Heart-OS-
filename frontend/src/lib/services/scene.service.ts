/**
 * Scene Service - API client for scene endpoints
 */
import { dedupedFetch } from './api/client';
import type { Scene } from '../types/shared-types';

export interface SceneResponse {
  id: string;
  name: string;
  description: string;
  config: Record<string, any>;
  image_path: string | null;
  created_at: string;
}

class SceneService {
  private basePath = '/api/v1/scenes';

  async generate(): Promise<SceneResponse[]> {
    return dedupedFetch<SceneResponse[]>(`${this.basePath}/generate`, {
      method: 'POST'
    });
  }

  async list(): Promise<SceneResponse[]> {
    return dedupedFetch<SceneResponse[]>(this.basePath, {
      cacheKey: 'scenes:list',
      cacheTtl: 120000
    });
  }

  async get(id: string): Promise<SceneResponse> {
    return dedupedFetch<SceneResponse>(`${this.basePath}/${id}`, {
      cacheKey: `scene:${id}`,
      cacheTtl: 120000
    });
  }
}

export const sceneService = new SceneService();
