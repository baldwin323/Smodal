
from typing import Any, Callable
from django.core.cache import cache
from functools import wraps
from Smodal.logging import logger


def cache_result(key: str) -> Callable:
    """
    This is a decorator that uses Django's caching mechanism to cache
    the result of any function it decorates. Ideal for resource-intensive,
    time-consuming functions that are called repeatedly with the same parameters.
    Caching these function results can markedly enhance the performance of the software.

    Parameters: 
    key (str): The key used for caching function result. Subsequent function calls 
    using the same parameters will use this key to look up in the cache, and if the result 
    is stored, it retrieves from there instead of re-running the entire function.
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # We form a complete key using the function name and its input arguments
                complete_key = f'{key}_{function.__name__}_{args}_{kwargs}'

                # We attempt to get a cached result
                result = cache.get(complete_key)

                # The result may not be cached, in which case we should compute it
                if result is None:
                    result = function(*args, **kwargs)

                    # After computing, it must be cached for future use
                    cache.set(complete_key, result)
                    logger.info(f'Result was not in cache, computed and added to cache with key {complete_key}')
                else:
                    logger.info(f'Result fetched from cache with key {complete_key}')

            except Exception as e:
                logger.error(f'An error occurred while caching the function result: {e}')

                # In case of error during caching, the execution of the function should continue
                result = function(*args, **kwargs)
            
            return result

        return wrapper

    return decorator
