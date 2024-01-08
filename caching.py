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

    Exception handling has been improved to handle scenarios when caching or retrieving from cache fails. Logging mechanism has 
    been enhanced to provide more detailed information about the errors.

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
                try:
                    logger.debug("Attempting to compute the result due to exception in cache access.")
                    result = function(*args, **kwargs)
                except Exception as e_sub:
                    logger.error(f'An error occurred while computing the result: {e_sub}')
                    raise e_sub   # an exception occurred while generating the result, it should rise upstream
            return result

        return wrapper

    return decorator