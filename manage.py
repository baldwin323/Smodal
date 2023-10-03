#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import execute_from_command_line

from Smodal.logging import logger  # Import the centralized logger

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smodal.settings')
    handle_migrations()
    execute_from_command_line(sys.argv)


def handle_migrations():
    """Run the necessary Django migrations."""
    try:
        execute_from_command_line(['./manage.py', 'makemigrations'])
        execute_from_command_line(['./manage.py', 'migrate'])
    except Exception as e:
        logger.exception('Migrations failed: {}'.format(e)) # Use the centralized logger here


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'startapp':
        start_application()
    else:
        main()