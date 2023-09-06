# Import Django's caching library
from django.core.cache import cache

def cache_result(key):
    """
    Caching decorator. Caches the result of a function using Django's 
    caching mechanism.
    Parameters: key (str): Cache key
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            # Attempt to get the cached result
            result = cache.get(key)

            # If the result was not cached, compute it
            if not result:
                result = function(*args, **kwargs)

                # Cache the result for future reference
                cache.set(key, result)

            return result
        return wrapper
    return decorator