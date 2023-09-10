#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import replit

# This is the main function. It runs administrative tasks.
def main():
    """Run administrative tasks."""
    
    is_replit = os.environ.get('REPLIT', False)

    # Here we specify the default settings module for the 'django-admin' utility to 
    # use when it runs. 
    if is_replit:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modaltokai.replit_settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modaltokai.settings')

    try:
        # Here we import execute_from_command_line from django.core.management,
        # it will be used to run Django administrative tasks.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # This error message will show up if you haven't installed Django, or have
        # forgotten to include it in your PYTHONPATH environment variable, or if you 
        # forgot to activate Python virtual environment.
        log_message = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )

        if is_replit:
            replit.log.error(log_message)
        else:
            logging.exception(log_message)
            
        raise exc

    # In this section, we run the necessary Django migrations using execute_from_command_line function.
    try:
        execute_from_command_line(['./manage.py', 'makemigrations'])
        execute_from_command_line(['./manage.py', 'migrate'])
    except Exception as e:
        # Log an error message if there's an exception while running migrations.
        if is_replit:
            replit.log.error("Exception in running Django migrations")
        else:
            logging.exception("Exception in running Django migrations", exc_info=True)
        raise e

    # Here, we are checking if all required packages are installed.
    required_packages = ['numpy', 'replit', 'Django', 'urllib3', 'requests', 'bootstrap4',
                         'pytest', 'pytest-django', 'django-debug-toolbar', 'logging', 'caching',
                         'django-allauth', 'django-crispy-forms', 'django-environ']
    installed_packages = [pkg.key for pkg in pkg_resources.working_set]
    for package in required_packages:
        if package not in installed_packages:
            # If a package is not installed, we log an error message and stop the program.
            if is_replit:
                replit.log.error(f"{package} is not installed. Please install required package.")
            else:
                logging.error(f"{package} is not installed. Please install required package.")
            sys.exit(1)

    # Lastly, we try to execute the command line commands
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        # If there's an error during execution, we log the error message and raise the exception.
        if is_replit:
            replit.log.error("Exception in command line execution:")
        else:
            logging.exception("Exception in command line execution:", exc_info=True)

        raise e

if __name__ == '__main__':
    # Setup the logging configuration. It creates or opens the file 'app.log' for writing and 
    # log messages of level 'ERROR' or higher are added to the file.
    is_replit = os.environ.get('REPLIT', False)
    if not is_replit: 
        logging.basicConfig(filename='app.log', filemode='w', level=logging.ERROR)

    # We call the main execution function to start the utility.
    main()