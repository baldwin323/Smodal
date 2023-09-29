import os
import my_logging.config
from django.conf import settings

# Creating a custom logger
logger = logging.getLogger(__name__)

# Loading logger configuration from settings
LOGGING_CONFIG = settings.LOGGING

# Configuring the logger
my_logging.config.dictConfig(LOGGING_CONFIG)