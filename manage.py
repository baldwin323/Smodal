#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pkg_resources
from django.core.management import execute_from_command_line

# Setting the environment variable 'MUTABLE_DEPLOY' to '1' when the server is run.
if 'runserver' in sys.argv:
    os.environ['MUTABLE_DEPLOY'] = '1'

REQUIRED_PACKAGES = [
    'numpy', 'replit', 'Django', 'urllib3', 'requests',
    'bootstrap4', 'pytest', 'pytest-django', 'django-debug-toolbar',
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
    execute_from_command_line(sys.argv)


def handle_migrations(is_replit):
    """Run the necessary Django migrations."""
    try:
        execute_from_command_line(['./manage.py', 'makemigrations'])
        execute_from_command_line(['./manage.py', 'migrate'])
    except Exception as e:
        raise e


def handle_error(message, exception, is_replit):
    """Handle any thrown exceptions and output to the correct log."""
    if is_replit:
        import replit
        replit.log.error(message)
    else:
        print(f"{message} : {exception}")


def check_packages(is_replit):
    """Check if all required packages are installed and update them if necessary."""
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    for package in REQUIRED_PACKAGES:
        if package not in installed_packages:
            handle_error("Attempted to perform a '--user' install. Please install the package in the virtual environment.", None, is_replit)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'startapp':
        start_application()
    else:
        main()