#!/usr/bin/env python3
"""
Django's command-line utility for administrative tasks.
This script is the entry point for running the Django application and handling essential tasks such as migrations.
This script uses argparse for command-line argument parsing for better maintainability and readability.
"""

import os
import sys
import subprocess
import argparse
from django.core.management import execute_from_command_line
from typing import NoReturn, Dict
from dotenv import load_dotenv
import logging

from Smodal.logging import logger  # Import the centralized logger

# Load environment variables
load_dotenv()

def main() -> NoReturn:
    """Run administrative tasks.
    This function configures the settings module and executes the command line arguments received.
    """

    parser = argparse.ArgumentParser(description="Run administrative tasks")
    parser.add_argument('--startapp', action='store_true', help='Start application')
    parser.add_argument('--buildcommands', action='store_true', help='Execute build commands')

    args = parser.parse_args()

    if args.startapp:
        start_application()
        return

    if args.buildcommands:
        build_commands()
        return

    if not os.getenv('DJANGO_SETTINGS_MODULE'):  # validate that the environment variable is set
        logger.error('The DJANGO_SETTINGS_MODULE environment variable must be set')
        return

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smodal.settings')
    try:
        handle_migrations()  # Running Django Migrations
        setup_frontend()  # Setup fronend
        print_env_variables()  # Print the environment variables
        execute_papertrail_setup()  # Execute papertrail setup
        execute_from_command_line(sys.argv)
    except Exception as e:
        logger.error(f'An error occurred in main: {e}')

def execute_papertrail_setup() -> NoReturn:
    """Execute the setup for Papertrail for centralized logging.
    """
    command = 'wget -qO - --header="X-Papertrail-Token: KvK5XeBIYkqZNCErbsD" https://papertrailapp.com/destinations/37343846/setup.sh | sudo bash'
    process = subprocess.Popen(command, shell=True)
    output, error = process.communicate()

def build_commands() -> NoReturn:
    """Execute necessary build commands for the application.
    """
    print("Building application...")

    # List of build commands
    commands = [["./manage.py", "collectstatic", "--noinput"],
                ["./manage.py", "makemigrations"],
                ["./manage.py", "migrate"]]

    for command in commands:
        try:
            execute_from_command_line(command)
            print(f'Successfully executed: {command}')
        except Exception as e:
            logger.exception(f'Executing command "{command}" failed: {e}')

    print("Building process completed!")

def setup_frontend() -> NoReturn:
    """Setup the Static files and media root configurations for the frontend.
    """

    # Placeholder for frontend setup
    # Add frontend specific setup code here.
    pass

def print_env_variables() -> Dict[str, str]:
    """Print all available environment variables and their corresponding keys.
    """
    try:
        env_vars = dict(os.environ.items())
        for key, value in env_vars.items():
            print(f"{key}: {value}")
        return env_vars
    except Exception as e:
        logger.error(f'An error occurred while printing environment variables: {e}')

def handle_migrations() -> NoReturn:
    """Run the Django migrations.
    """

    migration_commands = [['./manage.py', 'makemigrations'], ['./manage.py', 'migrate']]

    for command in migration_commands:
        try:
            execute_from_command_line(command)
        except Exception as e:
            logger.exception(f'Executing command "{command}" failed: {e}')

if __name__ == '__main__':
    main()