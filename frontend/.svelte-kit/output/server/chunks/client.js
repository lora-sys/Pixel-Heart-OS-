class ApiCache {
  constructor(defaultTtlMs = 6e4) {
    this.store = /* @__PURE__ */ new Map();
    this.defaultTtl = defaultTtlMs;
  }
  /**
   * Get value from cache if not expired.
   */
  get(key) {
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
  set(key, value, ttlMs) {
    const expiresAt = Date.now() + (ttlMs ?? this.defaultTtl);
    this.store.set(key, { value, expiresAt });
  }
  /**
   * Delete a specific cache key.
   */
  delete(key) {
    this.store.delete(key);
  }
  /**
   * Clear all cache entries.
   */
  clear() {
    this.store.clear();
  }
  /**
   * Invalidate all keys matching a pattern (prefix match).
   */
  invalidatePattern(prefix) {
    for (const key of this.store.keys()) {
      if (key.startsWith(prefix)) {
        this.store.delete(key);
      }
    }
  }
}
const apiCache = new ApiCache(6e4);
const API_BASE = "http://localhost:8000/api/v1";
const inFlightRequests = /* @__PURE__ */ new Map();
async function fetchJSON(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers
    },
    ...options
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }
  return res.json();
}
async function dedupedFetch(endpoint, options = {}) {
  const method = options.method || "GET";
  const isCacheable = method === "GET" || method === "";
  const cacheKey = options.cacheKey || (isCacheable ? `${method}${endpoint}${JSON.stringify(options.body || {})}` : null);
  if (isCacheable && cacheKey) {
    const cached = apiCache.get(cacheKey);
    if (cached !== null) {
      return cached;
    }
  }
  const dedupKey = `${method}${endpoint}${JSON.stringify(options.body || {})}`;
  if (inFlightRequests.has(dedupKey)) {
    return inFlightRequests.get(dedupKey);
  }
  const requestPromise = fetchJSON(endpoint, options).finally(() => {
    inFlightRequests.delete(dedupKey);
  });
  inFlightRequests.set(dedupKey, requestPromise);
  try {
    const result = await requestPromise;
    if (isCacheable && cacheKey) {
      apiCache.set(cacheKey, result, options.cacheTtl);
    }
    return result;
  } catch (error) {
    inFlightRequests.delete(dedupKey);
    throw error;
  }
}
export {
  dedupedFetch as d
};
