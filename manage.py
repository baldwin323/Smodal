#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pkg_resources
from django.core.management import execute_from_command_line
import time

# These are the required packages for Django and this utility to run.
REQUIRED_PACKAGES = ['numpy', 'replit', 'Django', 'urllib3', 'requests', 'bootstrap4',
                     'pytest', 'pytest-django', 'django-debug-toolbar', 'logging', 'caching',
                     'django-allauth', 'django-crispy-forms', 'django-environ']

def main():
    """Run administrative tasks."""
    
    is_replit = os.environ.get('REPLIT', False)

    # Here we specify the default settings module for the 'django-admin' utility to 
    # use when it runs. 
    if is_replit:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modaltokai.replit_settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modaltokai.settings')

    if is_replit:
        import replit

    # In this section, we run the necessary Django migrations using execute_from_command_line function.
    handle_migrations(is_replit)
    # Ensure all necessary packages are installed.
    check_packages(is_replit)

    # Execute any command line commands.
    handle_execution(is_replit)


def handle_migrations(is_replit):
    """Run the necessary Django migrations."""
    try:
        execute_from_command_line(['./manage.py', 'makemigrations'])
        execute_from_command_line(['./manage.py', 'migrate'])
    except Exception as e:
        # Log an error message if there's an exception while running migrations.
        handle_error("Exception in running Django migrations", e, is_replit)
        raise e


def handle_execution(is_replit):
    """Attempt to execute the command line commands."""
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        # If there's an error during execution, we log the error message and raise the exception.
        handle_error("Exception in command line execution:", e, is_replit)
        raise e


def handle_error(message, exception, is_replit):
    """Handle any thrown exceptions and output to the correct log."""
    if is_replit:
        replit.log.error(message)
    else:
        logging.exception(message, exc_info=True)
        

def check_packages(is_replit):
    """Check if all required packages are installed."""
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    for package in REQUIRED_PACKAGES:
        if package not in installed_packages:
            # If a package is not installed, we log an error message and stop the program.
            handle_error(f"{package} is not installed. Please install required package.", None, is_replit)

def start_application():
    """Starts the application with title page """
    execute_from_command_line(['./manage.py', 'runserver'])
    time.sleep(7)
    # Redirect to login page after 7 seconds
    # This will be handled in ./templates/index.html

if __name__ == '__main__':
    # We call the main execution function to start the utility.
    # If command is startapp we start the application
    if len(sys.argv) > 1 and sys.argv[1] == 'startapp':
        start_application()
    else:
        main()