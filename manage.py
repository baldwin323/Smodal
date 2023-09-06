```python
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging

def main():
    """Run administrative tasks."""
    # Specify the default settings module for the 'django-admin' utility to use when it runs. 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modaltokai.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logging.exception(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        raise exc

    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        logging.exception("Exception in command line execution:", exc_info=True)
        raise e

if __name__ == '__main__':
    # Setup logging configuration
    logging.basicConfig(filename='app.log', filemode='w', level=logging.ERROR)

    # Call the main execution function
    main()
```