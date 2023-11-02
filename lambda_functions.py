import json
import boto3
import os
import logging
import requests # for sending API requests
import zipfile
from datadog import initialize, api, statsd
from datadog.lambda_metric import lambda_stats

# Datadog integration - Initializing
options = {
    'api_key': os.environ['DATADOG_API_KEY'],
    'app_key': os.environ['DATADOG_APP_KEY']
}

initialize(**options)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

lambda_client = boto3.client('lambda')

# Function to make API call. This function will call the required API with the specified endpoint and payload.
# It will return the response of the API call.
def api_call(endpoint, payload=None, method="GET"):
    base_url = "http://api.example.com" # replace with your API base url
    headers = {"Content-Type": "application/json"}
    response = requests.request(method, base_url + endpoint, headers=headers, data=json.dumps(payload) if payload else None)
    return response.json()

# Function to register affiliate manager. It makes an API call to register an affiliate manager.
# In case of any errors, an exception is raised and logged.
def register_affiliate_manager(*args, **kwargs):
    try:
        # API integration
        result = api_call("/register_affiliate_manager", kwargs, "POST") # replace with your API endpoint
        return result
    except Exception as e:
        lambda_stats.increment('register_affiliate_manager.error')
        logger.error('An error occurred in register_affiliate_manager: %s', str(e))

# Function to monitor affiliated models. It makes an API call to keep track of affiliated models.
# An exception is raised and logged in case of any errors.
def monitor_affiliated_models(*args, **kwargs):
    try:
        # API integration
        result = api_call("/monitor_affiliated_models", kwargs, "POST") # replace with your API endpoint
        return result
    except Exception as e:
        lambda_stats.increment('monitor_affiliated_models.error')
        logger.error('An error occurred in monitor_affiliated_models: %s', str(e))

# Function to give credit when a new model signs up. The function makes an API call to provide credit.
# Exception handling is done to log any errors during the process.
def give_credit(*args, **kwargs):
    try:
        # API integration
        result = api_call("/give_credit", kwargs, "POST") # replace with your API endpoint
        return result
    except Exception as e:
        lambda_stats.increment('give_credit.error')
        logger.error('An error occurred in give_credit: %s', str(e))

operations = {
    'register_affiliate_manager': register_affiliate_manager, # Function call to register affiliate manager
    'monitor_affiliated_models': monitor_affiliated_models, # Function call to monitor affiliated models
    'give_credit': give_credit, # Function call for credit provision when new model signs up
}

# Lambda handler function instantiated for overall operations. It calls the corresponding function based on the
# operation passed in the event. Exception handling is performed to log any errors during the process.
def lambda_handler(event, context):
    try:
        operation = event['operation']

        # Validate the operation if it's in the defined operations
        if operation not in operations:
            raise ValueError(f'Invalid operation: {operation}')

        args = event.get('args', [])
        kwargs = event.get('kwargs', {})

        # Execute the operation with the provided args and kwargs
        result = operations[operation](*args, **kwargs)

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    except Exception as e:
        lambda_stats.increment('Smodal.lambda_functions.error')
        logger.error('An error occurred in lambda_handler: %s', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# New function to compress current directory into a zip file. The function walks through every directory and 
# its subdirectories and compresses all the files into a zip file.
def compress_directory():
    # Defining the name of the directory to be archived
    dir_name = '.'
    zipobj = zipfile.ZipFile('lambda_functions.zip', 'w', zipfile.ZIP_DEFLATED)

    # Iterate through all the directories and files in the specified directory
    for foldername, subfolders, filenames in os.walk(dir_name):
        for filename in filenames:
            # Create the complete filepath of the file in directory
            file = os.path.join(foldername, filename)
            # Add file to zip
            zipobj.write(file)
    zipobj.close()

# Call the function to compress directory into zip file
compress_directory()