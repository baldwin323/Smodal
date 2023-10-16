"""
WSGI config for django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Importing the custom logger from renamed logging file
from Smodal.logging import logger

# Set the DJANGO_SETTINGS_MODULE environment variable for deployment on DigitalOcean
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings.production')

# Ensuring logger configuration is correctly set up
try:
    logger.info("Setting up logging configuration...")
    application = get_wsgi_application()
except Exception as e:
    logger.error(f'Error setting up the logging configuration: {e}')
    raise
else:
    logger.info("Logging setup successful.")