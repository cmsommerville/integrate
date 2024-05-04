import json
from typing import Callable
from app.extensions import cache
from logger import logger


# Define a caching decorator
def cachedmethod(timeout=300):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            try:
                # Generate a memoized cache key
                cache_key = f"{func.__qualname__}::{hash((*args, *tuple(sorted(kwargs.items()))))}"
            except Exception:
                logger.warning(f"Could not memoize {func.__qualname__}")
                return func(*args, **kwargs)

            # Check if the response is already cached
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return json.loads(cached_value.decode())

            # Execute the function and cache the response
            result = func(*args, **kwargs)
            try:
                cache.setex(cache_key, timeout, json.dumps(result))
            except Exception:
                logger.warning(f"Could not set cache for cache key `{cache_key}`")

            return result

        return wrapper

    return decorator
