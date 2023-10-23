#!/usr/bin/env python3
"""
Django's command-line utility for administrative tasks.
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('SETTINGS_FILE', 'Smodal.settings'))
    try:
        # activate the virtual environment
        activate_venv_path = "/path/to/project/venv/bin/activate_this.py"
        with open(activate_venv_path) as f:
            exec(f.read(), dict(__file__=activate_venv_path))

        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f'An error occurred while trying to run command: {e}')
        
if __name__ == '__main__':
    main()