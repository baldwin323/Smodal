import os
import sys
import traceback
from logging import handlers
from django.conf import settings

# Initialize the project, build and new detailed loggers
project_logger = __import__('logging').getLogger(__name__)
build_logger = __import__('logging').getLogger('build_process')
detailed_logger = __import__('logging').getLogger('detailed')

# Load settings from configuration file
conf = settings.LOGGING
LOGGING_HOST = conf.get('LOGGING_HOST', 'localhost')
LOGGING_PORT = conf.get('LOGGING_PORT', 514)

# TeamCity specific settings
TEAMCITY_HOST = conf.get('TEAMCITY_HOST', 'localhost')
TEAMCITY_PORT = conf.get('TEAMCITY_PORT', 12345)

# Error handling for logging setup
try:
    # Setup handler with server info using SysLogHandler, the final destination for the log messages in TeamCity console
    handler = handlers.SysLogHandler(address=(TEAMCITY_HOST, TEAMCITY_PORT))
    handler.ident = "[Smodal.log] "  # prefix added to every log message to differentiate from other logs in system

    # Using a custom formatter for TeamCity
    # The message field has been changed to follow TeamCity's service messages format
    import logging
    formatter = logging.Formatter("%(levelname)s '%(__name__)s' - #%(funcName)s[%(pathname)s:%(lineno)d] %(message)s")
    handler.setFormatter(formatter)

    # Adding configured handler to the project, build and detailed loggers
    project_logger.addHandler(handler)
    build_logger.addHandler(handler)
    detailed_logger.addHandler(handler)

    # Configuring levels for loggers
    project_logger.setLevel(logging.DEBUG)
    build_logger.setLevel(logging.INFO)
    detailed_logger.setLevel(logging.DEBUG)
except Exception as e:
    project_logger.error('An error occurred while setting up the logger and formatter.', exc_info=True)

# Error handling for applying logger configuration
try:
    logging.config.dictConfig(conf)
except Exception as e:
    project_logger.error('An error occurred while applying the configuration to the logger. Error: %s', e, exc_info=True)

def handle_worktree_change_error(error_message: str):
    detailed_logger.error('Worktree contains unstaged changes. Exact Error: %s', error_message, exc_info=True)

def log_pactflow_response(headers: dict, body: str) -> None:
    try:
        detailed_logger.info('Pactflow Response Headers: %s', str(headers))
        detailed_logger.info('Pactflow Response Body: %s', body)
    except Exception as e:
        detailed_logger.error('An error occurred during the logging of pactflow response.', exc_info=True)

def log_build_process(msg: str, level: str = 'info') -> None:
    try:
        log_func = getattr(build_logger, level, None)
        if log_func:
            log_func(msg)
        else:
            build_logger.info(msg)
    except Exception as e:
        detailed_logger.error('An error occurred during the logging of build process.', exc_info=True)

def log_execution_details(func):
    def wrapper(*args, **kwargs):
        detailed_logger.info('Function %s called with args: %s, and kwargs: %s', func.__name__, args, kwargs)
        detailed_logger.info('Running function %s...', func.__name__)
        try:
            result = func(*args, **kwargs)
            detailed_logger.info('Function %s executed successfully.', func.__name__)
            return result
        except Exception as e:
            detailed_logger.error('An error occurred while running function %s.', func.__name__, exc_info=True)
            tb = traceback.format_exc()
            detailed_logger.error('Traceback:\n{}'.format(tb))
            raise e
    return wrapper

def uncaught_exception_handler(type, value, tb):
    detailed_logger.error('Uncaught exception: {}'.format(str(value)))
    tb = traceback.format_exception(type, value, tb)
    detailed_logger.error('Traceback: {}'.format(''.join(tb)))

sys.excepthook = uncaught_exception_handler