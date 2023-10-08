#!/usr/bin/env python3
"""
Django's command-line utility for administrative tasks.
This script is the entry point for running the Django application and handling essential tasks such as migrations.
"""
import os
import sys
from django.core.management import execute_from_command_line
from typing import NoReturn

from Smodal.logging import logger  # Import the centralized logger

def main() -> NoReturn:
    """Run administrative tasks.
    This function configures the settings module and executes the command line arguments received.
    """

    if not os.getenv('DJANGO_SETTINGS_MODULE'):  # validate that the environment variable is set
        raise ValueError('The DJANGO_SETTINGS_MODULE environment variable must be set')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smodal.settings')
    handle_migrations()
    execute_from_command_line(sys.argv)


def handle_migrations() -> NoReturn:
    """
    The handle_migrations method is responsible for running the Django migrations.
    It employs execute_from_command_line function from Django's management package to run the commands.
    In an event of an exception occurring while executing the commands, it captures it, logs a detailed message using the centralized logger, and continues to execute other commands.

    Exceptions:
    - SystemExit: If the command raises it, which might be for a number of reasons such as unapplied migrations.
    """

    migration_commands = [['./manage.py', 'makemigrations'], ['./manage.py', 'migrate']]

    for command in migration_commands:
        try:
            execute_from_command_line(command)
        except Exception as e:
            logger.exception(f'Executing command "{command}" failed: {e}')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'startapp':
        start_application()
    else:
        main()