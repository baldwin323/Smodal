# Import Django's caching library
# This library is essential for caching operations within this software. Caching speeds up certain operations by storing the result of expensive computations for quicker access at a later time.
from django.core.cache import cache

def cache_result(key):
    """
    Caching decorator. This decorator uses Django's caching mechanism to cache 
    the result of any function it decorates. Useful for expensive, time-consuming functions 
    that are called multiple times with the same parameters. Caching these function results 
    can greatly speed up the performance of the software.
    Parameters: 
    key (str): The key using which the function result will be cached. Future calls to the function 
    with the same parameters will look to the cache using this key, and if the result is stored, 
    it retrieves from there instead of re-running the entire function.
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            # Attempt to get the cached result
            # This step tries to see if a result is already computed and stored in cache against this key.
            result = cache.get(key)

            # If the result was not cached, compute it
            # If the result is not in cache, this means that this combination of parameters has not been seen before.
            # Therefore, call the function to compute the result of that function for this set of parameters.
            if not result:
                result = function(*args, **kwargs)

                # Cache the result for future reference
                # After computing the result, save it in the cache with the associated key for quick future reference.
                cache.set(key, result)

            return result
        return wrapper
    return decorator