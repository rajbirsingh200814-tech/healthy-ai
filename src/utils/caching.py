"""Rate limiting and caching utilities"""
from functools import wraps
from time import time
from typing import Dict, Any
import hashlib
import json
from slowapi import Limiter
from slowapi.util import get_remote_address


# Rate limiter
limiter = Limiter(key_func=get_remote_address)


class SimpleCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self, max_size: int = 100, ttl: int = 3600):
        self.cache: Dict[str, tuple] = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def _make_key(self, *args, **kwargs):
        """Generate cache key from args and kwargs"""
        key_data = json.dumps({
            'args': str(args),
            'kwargs': str(kwargs)
        }, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str):
        """Get value from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        self.cache[key] = (value, time())
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()


# Global cache instances
recommendation_cache = SimpleCache(max_size=200, ttl=1800)  # 30 min
analysis_cache = SimpleCache(max_size=500, ttl=3600)  # 1 hour


def cache_result(cache_obj: SimpleCache):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache_obj._make_key(*args, **kwargs)
            cached = cache_obj.get(key)
            
            if cached is not None:
                return cached
            
            result = func(*args, **kwargs)
            cache_obj.set(key, result)
            return result
        return wrapper
    return decorator
