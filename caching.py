
from typing import Any, Callable
from django.core.cache import cache
from functools import wraps
from Smodal.logging import logger

def cache_result(key: str) -> Callable:
    """
    This is a decorator that uses Django's caching mechanism to cache
    the result of any function it decorates. Ideal for resource-intensive,
    time-consuming functions that are called frequently with the same parameters.
    Caching these function results can markedly enhance the performance of the software.

    In case of exceptions during caching or retrieving from cache, the function
    continues its execution and a corresponding error message logged.

    Parameters: 
    key (str): The key used for caching function result. Subsequent function calls 
    using the same parameters will use this key to look up in the cache, and if the result 
    is stored, it retrieves from there instead of re-running the entire function.
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = None
            complete_key = f'{key}_{function.__name__}_{args}_{kwargs}'
            try:
                result = cache.get(complete_key)
                if result is None:
                    result = function(*args, **kwargs)
                    cache.set(complete_key, result)
                    logger.info(f'Result was not in cache, computed and added to cache with key {complete_key}')
                else:
                    logger.info(f'Result fetched from cache with key {complete_key}')
            except Exception as e:
                logger.error(f'An error occurred while fetching from cache or setting result into cache for key {complete_key} : {e}')
                if result is None:
                    result = function(*args, **kwargs)
            return result

        return wrapper

    return decorator