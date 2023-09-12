#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pkg_resources
from django.core.management import execute_from_command_line
import time

# Setting the environment variable 'MUTABLE_DEPLOY' to '1' when the server is run.
if 'runserver' in sys.argv:
    os.environ['MUTABLE_DEPLOY'] = '1'

execute_from_command_line(sys.argv)

REQUIRED_PACKAGES = [
    'numpy', 'replit', 'Django', 'urllib3', 'requests', 'bootstrap4',
    'pytest', 'pytest-django', 'django-debug-toolbar', 'logging', 'caching',
    'django-allauth', 'django-crispy-forms', 'django-environ'
]

def main():
    """Run administrative tasks."""

    is_replit = os.environ.get('REPLIT', False)

    if is_replit:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modaltokai.replit_settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modaltokai.settings')

    if is_replit:
        import replit

    handle_migrations(is_replit)
    check_packages(is_replit)
    handle_execution(is_replit)


def handle_migrations(is_replit):
    """Run the necessary Django migrations."""
    try:
        execute_from_command_line(['./manage.py', 'makemigrations'])
        execute_from_command_line(['./manage.py', 'migrate'])
    except Exception as e:
        handle_error("Exception in running Django migrations", e, is_replit)
        raise e


def handle_execution(is_replit):
    """Attempt to execute the command line commands."""
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
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
            handle_error("Attempted to perform a '--user' install. Please install the package in the virtual environment.", None, is_replit)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'startapp':
        start_application()
    else:
        main()