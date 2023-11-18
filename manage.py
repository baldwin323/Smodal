#!/usr/bin/env python3.12
"""
Django's command-line utility for administrative tasks.
This script also handles exception reporting and replaces the previous
logging mechanism used by sys.stdout with one that uses environment variables for credentials.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    # Try to import django
    import django
    from django.core.management import execute_from_command_line
except ModuleNotFoundError:
    # Log the error and exit if import fails
    print("Error: Django module not found.")
    exit(1)

def main():
    """
    Run administrative tasks.
    Activates the python environment and runs the gunicorn server.
    Exception handling replaced, no longer communicates with datadog.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('SETTINGS_FILE', 'Smodal.settings'))
    
    try:
        # Activate the virtual environment
        # This raises an exception if the path doesn't exist or the file cannot be read
        activate_venv_path = "/path/to/project/venv/bin/activate_this.py"
        with open(activate_venv_path) as f:
            exec(f.read(), dict(__file__=activate_venv_path))

        # Modify the run command
        # This runs the gunicorn server with specific settings
        os.system("gunicorn --worker-tmp-dir /dev/shm Smodal.wsgi")
        
    except Exception as e:
        print(f'An error occurred while trying to run command: {e}')

        # Previous integration with datadog has been removed. Now logging exceptions to stdout
        print(f"Exception in manage.py: An error occurred while trying to run command: {e}")

        print("Execution of the new plan was unsuccessful. Please review and rectify the errors.")
        
if __name__ == '__main__':
    main()
