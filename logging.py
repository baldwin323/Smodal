import os
from logging.handlers import SysLogHandler
from django.conf import settings

project_logger = __import__('logging').getLogger(__name__)

LOGGING_CONFIG = settings.LOGGING

# Papertrail specific settings
PAPERTRAIL_HOST = 'logs.papertrailapp.com'
PAPERTRAIL_PORT = 12345  # Replace with your Papertrail port

LOGGING_HOST = os.getenv('LOGGING_HOST', 'localhost')

LOGGING_PORT = os.getenv('LOGGING_PORT', 514)

try:
    handler = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
    formatter = __import__('logging').Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    project_logger.addHandler(handler)
except Exception as e:
    project_logger.error(f'An error occurred while setting up the handler: {e}')

try:
    __import__('logging').config.dictConfig(LOGGING_CONFIG)
except Exception as e:
    project_logger.error(f'An error occurred while applying logger configuration: {e}')

# New logger to handle build process logging
build_logger = __import__('logging').getLogger('build_process')
project_logger.addHandler(build_logger)


def log_pactflow_response(headers: dict, body: str) -> None:
    try:
        project_logger.info('Pactflow Response Headers: %s', str(headers))
        project_logger.info('Pactflow Response Body: %s', body)
    except Exception as e:
        project_logger.error(f'An error occurred during logging of pactflow response: {e}')


# New function to log build process details
def log_build_process(msg: str, level: str = 'info') -> None:
    log_func = getattr(build_logger, level, build_logger.info)
    log_func(msg)