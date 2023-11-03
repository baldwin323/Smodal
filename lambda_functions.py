import json
import boto3
import os
import logging
import requests # for sending API requests
import zipfile
# Removed datadog integration because we are no longer using DigitalOcean
from boto3.session import Session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Fetching AWS Access Key, Secret Key and Region from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', None)
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', None)
aws_region = os.getenv('AWS_REGION', None)

# Create a Boto3 session using the fetched AWS credentials
session = Session(aws_access_key_id=aws_access_key_id, 
                  aws_secret_access_key=aws_secret_access_key, 
                  region_name=aws_region)

lambda_client = session.client('lambda')

def api_call(endpoint, payload=None, method="GET"):
    base_url = "http://api.example.com" # replace with your API base url
    headers = {"Content-Type": "application/json"}
    response = requests.request(method, base_url + endpoint, headers=headers, data=json.dumps(payload) if payload else None)
    return response.json()

def register_affiliate_manager(*args, **kwargs):
    try:
        # API integration
        result = api_call("/register_affiliate_manager", kwargs, "POST") # replace with your API endpoint
        return result
    except Exception as e:
        logger.error('An error occurred in register_affiliate_manager: %s', str(e))

def monitor_affiliated_models(*args, **kwargs):
    try:
        # API integration
        result = api_call("/monitor_affiliated_models", kwargs, "POST") # replace with your API endpoint
        return result
    except Exception as e:
        logger.error('An error occurred in monitor_affiliated_models: %s', str(e))

def give_credit(*args, **kwargs):
    try:
        # API integration
        result = api_call("/give_credit", kwargs, "POST") # replace with your API endpoint
        return result
    except Exception as e:
        logger.error('An error occurred in give_credit: %s', str(e))

operations = {
    'register_affiliate_manager': register_affiliate_manager, # Function call to register affiliate manager
    'monitor_affiliated_models': monitor_affiliated_models, # Function call to monitor affiliated models
    'give_credit': give_credit, # Function call for credit provision when new model signs up
}

def lambda_handler(event, context):
    try:
        operation = event['operation']

        if operation not in operations:
            raise ValueError(f'Invalid operation: {operation}')

        args = event.get('args', [])
        kwargs = event.get('kwargs', {})

        result = operations[operation](*args, **kwargs)

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    except Exception as e:
        logger.error('An error occurred in lambda_handler: %s', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
def compress_directory():
    dir_name = '.'
    zipobj = zipfile.ZipFile('lambda_functions.zip', 'w', zipfile.ZIP_DEFLATED)

    for foldername, subfolders, filenames in os.walk(dir_name):
        for filename in filenames:
            file = os.path.join(foldername, filename)
            zipobj.write(file)
    zipobj.close()

compress_directory()