import os
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

try:
    # Setup handler with server info
    handler = handlers.SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
    
    # Define and set formatter for clarity and precise information
    formatter = __import__('logging').Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    
    # Add the handler to the project logger
    project_logger.addHandler(handler)
except Exception as e:
    project_logger.error('An error occurred while setting up the logger and formatter.', exc_info=True)

try:
    # Apply the loaded configuration to the logger
    __import__('logging').config.dictConfig(conf)
except Exception as e:
    project_logger.error('An error occurred while applying logger configuration.', exc_info=True)

# Add the new build logger to the project logger
project_logger.addHandler(build_logger)

def log_pactflow_response(headers: dict, body: str) -> None:
    """
    Logs the Pactflow response headers and body.

    :param headers: The response headers
    :param body: The response body
    """
    try:
        project_logger.info('Pactflow Response Headers: %s', str(headers))
        project_logger.info('Pactflow Response Body: %s', body)
    except Exception as e:
        project_logger.error('An error occurred during logging of pactflow response.', exc_info=True)

def log_build_process(msg: str, level: str = 'info') -> None:
    """
    Logs the build process at the specified level.

    :param msg: The message to log
    :param level: The logging level (defaults to 'info')
    """
    try:
        log_func = getattr(build_logger, level, build_logger.info)
        log_func(msg)
    except Exception as e:
        project_logger.error('An error occurred during logging of build process.', exc_info=True)