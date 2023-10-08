
import logging
import os
from logging.handlers import SysLogHandler
from django.conf import settings

# Custom logger is created with the following line.
logger = logging.getLogger(__name__)

# The logger configuration present in the settings.
LOGGING_CONFIG = settings.LOGGING  # type: dict

# Here we set the host for Graylog or Logstash. 'localhost' is default.
LOGGING_HOST = os.getenv('LOGGING_HOST', 'localhost')  # type: str

# The Syslog UDP port for Graylog or Logstash. Default is port 514.
LOGGING_PORT = os.getenv('LOGGING_PORT', 514)  # type: int

try:
    # We're setting up a centralized logger.
    handler = SysLogHandler(address=(LOGGING_HOST, LOGGING_PORT))  # type: SysLogHandler
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')  # type: logging.Formatter
    handler.setFormatter(formatter)
    logger.addHandler(handler)
except Exception as e:  # type: Exception
    logger.error(f'An error occurred while setting up the handler: {e}')

try:
    # Applying LOGGING_CONFIG
    logging.config.dictConfig(LOGGING_CONFIG)
except Exception as e:  # type: Exception
    logger.error(f'An error occurred while applying logger configuration: {e}')

def log_pactflow_response(headers: dict, body: str) -> None:
    """
    Logs the pactflow response. It takes both headers and body as inputs.

    :param headers: Response headers from pactflow
    :param body: Response body from pactflow
    :return: None
    """
    try:
        # Log the pactflow response headers
        logger.info('Pactflow Response Headers: %s', str(headers))
        # Log the pactflow response body
        logger.info('Pactflow Response Body: %s', body)
    except Exception as e:  # type: Exception
        logger.error(f'An error occurred during logging of pactflow response: {e}')