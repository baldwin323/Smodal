# Importing Django's caching library and functools for wrapping metadata
from django.core.cache import cache
from functools import wraps

def cache_result(key):
    """
    This decorator uses Django's caching mechanism to cache 
    the result of any function it decorates. Ideal for resource-intensive, time-consuming functions 
    that are invoked repeatedly with identical parameters. Caching these function results 
    can appreciably enhance the software's performance.
    Parameters: 
    key (str): The key used to cache the function result. Subsequent calls to the function 
    with the same parameters will lookup in the cache using this key, and if the result is stored, 
    it retrieves from there instead of re-running the entire function.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Forming the complete key with function name and input arguments
            complete_key = f'{key}_{function.__name__}_{str(args)}_{str(kwargs)}'
            # Attempt to get the cached result
            result = cache.get(complete_key)

            # In case the result is not cached, compute it
            if result is None:
                result = function(*args, **kwargs)

                # Cache the result for future use
                cache.set(complete_key, result)

            return result
        return wrapper
    return decorator