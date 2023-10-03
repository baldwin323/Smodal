#!/usr/bin/env python3
"""
Django's command-line utility for administrative tasks.
This script is the entry point for running the Django application and handling essential tasks such as migrations.
"""
import os
import sys
from django.core.management import execute_from_command_line

from Smodal.logging import logger  # Import the centralized logger


def main():
    """Run administrative tasks.
    This function configures the settings module and executes the command line arguments received.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smodal.settings')
    handle_migrations()
    execute_from_command_line(sys.argv)


def handle_migrations():
    """
    The handle_migrations method is responsible for running the Django migrations.
    It employs execute_from_command_line function from Django's management package to run the commands.
    In an event of an exception occurring while executing the commands, it captures it, logs a detailed message using the centralized logger, and continues to execute other commands.

    Exceptions:
    - SystemExit: If the command raises it, which might be for a number of reasons such as unapplied migrations.
    """
    try:
        execute_from_command_line(['./manage.py', 'makemigrations'])
    except Exception as e:
        logger.exception(f'Creating migrations failed: {e}')
    try:
        execute_from_command_line(['./manage.py', 'migrate'])
    except Exception as e:
        logger.exception(f'Applying migrations failed: {e}')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'startapp':
        start_application()
    else:
        main()