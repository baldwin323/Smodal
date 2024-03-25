
"""
ASGI config for django_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

# Ensure that the DJANGO_SETTINGS_MODULE environment variable is set correctly for deployment on DigitalOcean.
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'

# Import logging before getting the asgi application to ensure logging setup happens first
import Smodal.logging

from django.core.asgi import get_asgi_application

application = get_asgi_application()