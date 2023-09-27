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
    'numpy', 'Django', 'urllib3', 'requests',
    'bootstrap4', 'pytest', 'pytest-django', 'django-debug-toolbar',
    'django-allauth', 'django-crispy-forms', 'django-environ'
]

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modaltokai.settings')
    handle_migrations()
    check_packages()
    execute_from_command_line(sys.argv)


def handle_migrations():
    """Run the necessary Django migrations."""
    try:
        execute_from_command_line(['./manage.py', 'makemigrations'])
        execute_from_command_line(['./manage.py', 'migrate'])
    except Exception as e:
        print('Migrations failed: {}'.format(e))


def check_packages():
    """Check if all required packages are installed and update them if necessary."""
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    for package in REQUIRED_PACKAGES:
        if package not in installed_packages:
            print('Package {} is not installed'.format(package))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'startapp':
        start_application()
    else:
        main()