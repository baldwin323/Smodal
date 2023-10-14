"""
WSGI config for django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the DJANGO_SETTINGS_MODULE environment variable for deployment on DigitalOcean
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings.production'

application = get_wsgi_application()