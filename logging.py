import os
import traceback
from logging import handlers
from django.conf import settings

# Initialize the project and build loggers
project_logger = __import__('logging').getLogger(__name__)
build_logger = __import__('logging').getLogger('build_process')

# Load settings from configuration file
conf = settings.LOGGING
LOGGING_HOST = conf.get('LOGGING_HOST', 'localhost')
LOGGING_PORT = conf.get('LOGGING_PORT', 514)

# Papertrail specific settings
PAPERTRAIL_HOST = conf.get('PAPERTRAIL_HOST', 'logs.papertrailapp.com')
PAPERTRAIL_PORT = conf.get('PAPERTRAIL_PORT', 12345) 

# Error handling for logging setup
try:
    # Setup handler with server info using SysLogHandler
    handler = handlers.SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
    
    # Using a precise and clear formatter for better understanding
    formatter = __import__('logging').Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    
    # Adding configured handler to the project logger
    project_logger.addHandler(handler)
except Exception as e:
    project_logger.error('An error occurred while setting up the logger and formatter.', exc_info=True)

# Error handling for applying logger configuration
try:
    __import__('logging').config.dictConfig(conf)
except Exception as e:
    project_logger.error('An error occurred while applying the configuration to the logger. Error: %s', e, exc_info=True)

def log_pactflow_response(headers: dict, body: str) -> None:
    """
    The purpose of this function is to log the Pactflow response headers and body.

    :param headers: These are the response headers received
    :param body: This is the response body received
    """
    try:
        project_logger.info('Pactflow Response Headers: %s', str(headers))
        project_logger.info('Pactflow Response Body: %s', body)
    except Exception as e:
        # Error Handling for Pactflow responses logging
        project_logger.error('An error occurred during the logging of pactflow response.', exc_info=True)

def log_build_process(msg: str, level: str = 'info') -> None:
    """
    Function to log the build process at the specific level.

    :param msg: String message to be logged
    :param level: Logging level (default='info')
    """
    try:
        log_func = getattr(build_logger, level, build_logger.info)
        log_func(msg)
    except Exception as e:
        # Error Handling for build process logging
        project_logger.error('An error occurred during the logging of build process.', exc_info=True)

def log_execution_details(func):
    """
    This is a modified decorator function to log detailed execution information of the decorated function.

    :param func: The function for which execution details are logged
    """
    def wrapper(*args, **kwargs):
        # Provides the details of the function, its arguments and keyword arguments
        project_logger.info('Function %s called with args: %s, and kwargs: %s', func.__name__, args, kwargs)
        project_logger.info('Running function %s...', func.__name__)

        try:
            result = func(*args, **kwargs)
            # Success logging for function execution
            project_logger.info('Function %s executed successfully.', func.__name__)
            return result
        except Exception as e:
            # Error handling for function execution
            project_logger.error('An error occurred while running function %s.', func.__name__, exc_info=True)
            # Adding more information about the error
            tb = traceback.format_exc()
            project_logger.error(f"Traceback:\n {tb}")
            raise e
    return wrapper

# Function to handle logging for uncaught exceptions
def uncaught_exception_handler(type, value, tb):
    """
    This function is to handle uncaught exceptions and log them

    :param type: Exception Type
    :param value: Exception Value
    :param tb: Traceback
    """
    project_logger.error("Uncaught exception: {0}".format(str(value)))
    project_logger.error(''.join(traceback.format_tb(tb)))

# Sets the function "uncaught_exception_handler" as the handler for unhandled exceptions
sys.excepthook = uncaught_exception_handler
