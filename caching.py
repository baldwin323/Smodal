# Importing Django's caching library and functools for wrapping metadata
from django.core.cache import cache
from functools import wraps

def cache_result(key):
    """
    Caching decorator optimized for Replit. This decorator uses Django's caching mechanism to cache 
    the result of any function it decorates. Useful for expensive, time-consuming functions 
    that are called multiple times with the same parameters. Caching these function results 
    can significantly speed up the software's performance.
    Parameters: 
    key (str): The key using which the function result will be cached. Future calls to the function 
    with the same parameters will look to the cache using this key, and if the result is stored, 
    it retrieves from there instead of re-running the entire function.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Constructing the complete key with function name and passed arguments
            complete_key = f'{key}_{function.__name__}_{str(args)}_{str(kwargs)}'
            # Attempt to get the cached result
            # This step tries to see if a result is already computed and stored in cache against this complete_key.
            result = cache.get(complete_key)

            # If the result was not cached, compute it
            # If the result is not in cache, this means that this combination of parameters and function has not been seen before.
            # Therefore, we call the function to compute the result for this set of parameters.
            if result is None:
                result = function(*args, **kwargs)

                # Cache the result for future reference
                # After computing the result, we save it in the cache with the associated complete_key for quick future reference.
                cache.set(complete_key, result)

            return result
        return wrapper
    return decorator