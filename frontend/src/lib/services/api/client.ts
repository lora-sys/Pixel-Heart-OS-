/**
 * API Client - Base HTTP client with interceptors
 */
import { apiCache, invalidateCache } from '../../cache/api-cache';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface RequestConfig extends RequestInit {
  cacheKey?: string;
  cacheTtl?: number;
}

/**
 * Centralized fetch with error handling and caching
 */
export async function apiFetch<T>(
  endpoint: string,
  config: RequestConfig = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const { cacheKey, cacheTtl, ...fetchConfig } = config;

  // Check cache for GET requests
  if (fetchConfig.method !== 'POST' && fetchConfig.method !== 'PATCH' && cacheKey) {
    const cached = apiCache.get<T>(cacheKey);
    if (cached) {
      return cached;
    }
  }

  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...fetchConfig.headers
      },
      ...fetchConfig
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    const data = await response.json();

    // Cache successful GET responses
    if (fetchConfig.method !== 'POST' && fetchConfig.method !== 'PATCH' && cacheKey) {
      apiCache.set(cacheKey, data, cacheTtl);
    }

    // Invalidate relevant cache keys on mutations
    if (fetchConfig.method === 'POST' || fetchConfig.method === 'PATCH' || fetchConfig.method === 'DELETE') {
      invalidateCache('heroine:');
      invalidateCache('npcs:');
      invalidateCache('beads:');
      invalidateCache('simulation:');
    }

    return data;
  } catch (error) {
    console.error(`API Error [${fetchConfig.method || 'GET'} ${endpoint}]:`, error);
    throw error;
  }
}

/**
 * Cancelable fetch wrapper (for request deduplication)
 */
const pendingRequests = new Map<string, Promise<any>>();

export export async function dedupedFetch<T>(
  endpoint: string,
  config: RequestConfig = {}
): Promise<T> {
  const key = `${endpoint}:${JSON.stringify(config)}`;

  if (pendingRequests.has(key)) {
    return pendingRequests.get(key)!;
  }

  const promise = apiFetch<T>(endpoint, config)
    .finally(() => {
      pendingRequests.delete(key);
    });

  pendingRequests.set(key, promise);
  return promise;
}
