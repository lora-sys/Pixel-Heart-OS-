/**
 * In-memory API response cache with TTL.
 * Simple LRU-like cache for frequently accessed data.
 */
interface CacheEntry<T> {
  value: T;
  expiresAt: number; // timestamp in ms
}

export class ApiCache {
  private store: Map<string, CacheEntry<any>> = new Map();
  private defaultTtl: number;

  constructor(defaultTtlMs: number = 60000) {
    this.defaultTtl = defaultTtlMs;
  }

  /**
   * Get value from cache if not expired.
   */
  get<T>(key: string): T | null {
    const entry = this.store.get(key);
    if (!entry) return null;

    if (Date.now() > entry.expiresAt) {
      this.store.delete(key);
      return null;
    }

    return entry.value;
  }

  /**
   * Set cache value with TTL.
   */
  set<T>(key: string, value: T, ttlMs?: number): void {
    const expiresAt = Date.now() + (ttlMs ?? this.defaultTtl);
    this.store.set(key, { value, expiresAt });
  }

  /**
   * Delete a specific cache key.
   */
  delete(key: string): void {
    this.store.delete(key);
  }

  /**
   * Clear all cache entries.
   */
  clear(): void {
    this.store.clear();
  }

  /**
   * Invalidate all keys matching a pattern (prefix match).
   */
  invalidatePattern(prefix: string): void {
    for (const key of this.store.keys()) {
      if (key.startsWith(prefix)) {
        this.store.delete(key);
      }
    }
  }
}

// Global singleton instance
export const apiCache = new ApiCache(60000); // 1 minute default TTL
