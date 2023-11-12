```python
import json
import boto3
import os
import logging
import requests # for sending API requests
import zipfile
from boto3.session import Session

# Setting up logger
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

# Generic function to make API calls
def api_call(endpoint, payload=None, method="GET"):
    base_url = "http://api.example.com" # replace with your API base url
    headers = {"Content-Type": "application/json"}
    # Enhanced error handling
    try:
        response = requests.request(method, base_url + endpoint, headers=headers, 
                                    data=json.dumps(payload) if payload else None)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error occurred in api_call: %s", errh)
    except requests.exceptions.ConnectionError as errc:
        logger.error("Error Connecting occurred in api_call: %s", errc)
    except requests.exceptions.Timeout as errt:
        logger.error("Timeout Error occurred in api_call: %s", errt)
    except requests.exceptions.RequestException as err:
        logger.error("OOps: Something Else occurred in api_call: %s", err)  
    return response.json()

def register_affiliate_manager(*args, **kwargs):
    # API integration
    return api_call("/register_affiliate_manager", kwargs, "POST")

def monitor_affiliated_models(*args, **kwargs):
    # API integration
    return api_call("/monitor_affiliated_models", kwargs, "POST")

def give_credit(*args, **kwargs):
    # API integration
    return api_call("/give_credit", kwargs, "POST")

operations = {
    # Map operations to related function call
    'register_affiliate_manager': register_affiliate_manager,
    'monitor_affiliated_models': monitor_affiliated_models,
    'give_credit': give_credit,
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
        logger.error('An error occurred in lambda_handler: %s', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Function to perform directory compression
def compress_directory():
    dir_name = '.'
    zipobj = zipfile.ZipFile('lambda_functions.zip', 'w', zipfile.ZIP_DEFLATED)
    for foldername, subfolders, filenames in os.walk(dir_name):
        for filename in filenames:
            file = os.path.join(foldername, filename)
            zipobj.write(file)
    zipobj.close()

# Compression execution
compress_directory()
```
