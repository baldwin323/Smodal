
#!/usr/bin/env python3
"""
Django's command-line utility for administrative tasks.
This script also handles exception reporting and logging for the Django application.
Now utilizing MongoDB for these functionalities.
"""

import os
import sys

# Import pymongo
from pymongo import MongoClient

# Create a connection to MongoDB
client = MongoClient("mongodb+srv://username:password@cluster.region.mongodb.net/database?retryWrites=true&w=majority") 
db = client['database_name']

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
    Exception handling is in place to report errors to MongoDB and stdout.
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

        # Instead of sending the exception to datadog, now insert it into the MongoDB
        collection = db['errors']
        error_report = {
            'title': "Exception in manage.py",
            'text': f'An error occurred while trying to run command: {e}',
            'tags': ['application:Smodal', 'environment:development']
        }
        collection.insert_one(error_report)

        # Update the main function to handle any exceptions occurred during the execution of the new plan
        print("Execution of the plan was unsuccessful. Please review and rectify the errors.")
        
if __name__ == '__main__':
    main()