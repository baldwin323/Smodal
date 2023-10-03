
import logging
import os
from logging.handlers import SysLogHandler
from django.conf import settings

# Creating a custom logger
logger = logging.getLogger(__name__)

# Loading logger configuration from settings
LOGGING_CONFIG = settings.LOGGING

# Graylog or Logstash host
LOGGING_HOST = os.getenv('LOGGING_HOST', 'localhost')

# Syslog UDP port for Graylog or Logstash 
LOGGING_PORT = os.getenv('LOGGING_PORT', 514)

# Configuring the centralized logger
handler = SysLogHandler(address=(LOGGING_HOST, LOGGING_PORT))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(formatter)
logger.addHandler(handler)
        
# Applying configuration
logging.config.dictConfig(LOGGING_CONFIG)