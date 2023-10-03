
import logging
import os
from logging.handlers import SysLogHandler
from django.conf import settings

# Custom logger is created with the following line.
logger = logging.getLogger(__name__)

# Logger configuration is grabbed from settings.
LOGGING_CONFIG = settings.LOGGING

# Here we have the Graylog or Logstash host. Default is 'localhost'.
LOGGING_HOST = os.getenv('LOGGING_HOST', 'localhost')

# The Syslog UDP port for Graylog or Logstash is defined here. Default is 514.
LOGGING_PORT = os.getenv('LOGGING_PORT', 514)

try:
    # Centralized logger gets configured.
    handler = SysLogHandler(address=(LOGGING_HOST, LOGGING_PORT))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

except Exception as e:
    logger.error('An error occurred while setting up the handler: {}'.format(e))

try:
    # Applying the above configuration
    logging.config.dictConfig(LOGGING_CONFIG)
    
except Exception as e:
    logger.error('An error occurred while applying logger configuration: {}'.format(e))

# Function logs the pactflow response. It takes both headers and body as inputs.
def log_pactflow_response(headers, body):
    try:
        # Logging the pactflow response headers
        logger.info('Pactflow Response Headers: %s', str(headers))
        # Logging the pactflow response body
        logger.info('Pactflow Response Body: %s', str(body))
        
    except Exception as e:
        logger.error('An error occurred during logging of pactflow response: {}'.format(e))