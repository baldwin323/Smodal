import os
from logging.handlers import SysLogHandler
from django.conf import settings

# Rename the file to project_logging to avoid conflict with built-in logging
# Creating a custom logger
project_logger = __import__('logging').getLogger(__name__)

# Setting the logger configuration from settings
LOGGING_CONFIG = settings.LOGGING  # type: dict

# Setting up the host for Graylog or Logstash. Defaults to 'localhost'
LOGGING_HOST = os.getenv('LOGGING_HOST', 'localhost')  # type: str

# Setting up the Syslog UDP port for Graylog or Logstash. Defaults to port 514
LOGGING_PORT = os.getenv('LOGGING_PORT', 514)  # type: int

try:
    # Setting up centralized logger
    handler = SysLogHandler(address=(LOGGING_HOST, LOGGING_PORT))  # type: SysLogHandler
    formatter = __import__('logging').Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')  # type: __import__('logging').Formatter
    handler.setFormatter(formatter)
    project_logger.addHandler(handler)
except Exception as e:  # type: Exception
    project_logger.error(f'An error occurred while setting up the handler: {e}')

try:
    # Apply LOGGING_CONFIG
    __import__('logging').config.dictConfig(LOGGING_CONFIG)
except Exception as e:  # type: Exception
    project_logger.error(f'An error occurred while applying logger configuration: {e}')


def log_pactflow_response(headers: dict, body: str) -> None:
    """
    Function to log the pactflow response.

    Params:
    headers: dict - Response headers from pactflow
    body: str - Response body from pactflow

    Returns:
    None

    """
    try:
        # Log the pactflow response headers
        project_logger.info('Pactflow Response Headers: %s', str(headers))
        # Log the pactflow response body
        project_logger.info('Pactflow Response Body: %s', body)
    except Exception as e:  # type: Exception
        project_logger.error(f'An error occurred during logging of pactflow response: {e}')