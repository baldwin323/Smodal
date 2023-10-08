import logging
import os
from logging.handlers import SysLogHandler
from django.conf import settings

# Creating a custom logger
logger = logging.getLogger(__name__)

# Setting the logger configuration from settings
LOGGING_CONFIG = settings.LOGGING  # type: dict

# Setting up the host for Graylog or Logstash. Defaults to 'localhost'
LOGGING_HOST = os.getenv('LOGGING_HOST', 'localhost')  # type: str

# Setting up the Syslog UDP port for Graylog or Logstash. Defaults to port 514
LOGGING_PORT = os.getenv('LOGGING_PORT', 514)  # type: int

try:
    # Setting up centralized logger
    handler = SysLogHandler(address=(LOGGING_HOST, LOGGING_PORT))  # type: SysLogHandler
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')  # type: logging.Formatter
    handler.setFormatter(formatter)
    logger.addHandler(handler)
except Exception as e:  # type: Exception
    logger.error(f'An error occurred while setting up the handler: {e}')

try:
    # Apply LOGGING_CONFIG
    logging.config.dictConfig(LOGGING_CONFIG)
except Exception as e:  # type: Exception
    logger.error(f'An error occurred while applying logger configuration: {e}')


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
        logger.info('Pactflow Response Headers: %s', str(headers))
        # Log the pactflow response body
        logger.info('Pactflow Response Body: %s', body)
    except Exception as e:  # type: Exception
        logger.error(f'An error occurred during logging of pactflow response: {e}')