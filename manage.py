#!/usr/bin/env python3
"""
Django's command-line utility for administrative tasks.
"""
import os
import sys
from django.core.management import execute_from_command_line

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smodal.settings')
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f'An error occurred in main: {e}')
        
if __name__ == '__main__':
    main()