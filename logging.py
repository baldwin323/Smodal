import logging.config
import os
from django.conf import settings

# Creating a custom logger
logger = logging.getLogger(__name__)

# Loading logger configuration from settings
LOGGING_CONFIG = settings.LOGGING

# Configuring the logger
logging.config.dictConfig(LOGGING_CONFIG)