"""
In-memory cache with TTL support.
Simple LRU-like cache for frequently accessed data.
"""
import time
from typing import Optional, Any, Dict
from threading import RLock


class Cache:
    """Thread-safe in-memory cache with TTL."""

    def __init__(self, default_ttl: int = 60):
        """
        Initialize cache.

        Args:
            default_ttl: Default time-to-live in seconds
        """
        self._store: Dict[str, tuple[Any, float]] = {}
        self._default_ttl = default_ttl
        self._lock = RLock()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        with self._lock:
            if key not in self._store:
                return None

            value, expires_at = self._store[key]
            if time.time() > expires_at:
                del self._store[key]
                return None

            return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cache value with TTL."""
        with self._lock:
            if ttl is None:
                ttl = self._default_ttl
            expires_at = time.time() + ttl
            self._store[key] = (value, expires_at)

    def delete(self, key: str) -> None:
        """Remove key from cache."""
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._store.clear()

    def invalidate_pattern(self, pattern: str) -> None:
        """Invalidate all keys matching pattern (simple prefix match)."""
        with self._lock:
            keys_to_delete = [k for k in self._store.keys() if k.startswith(pattern)]
            for key in keys_to_delete:
                del self._store[key]
