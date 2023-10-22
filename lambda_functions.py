import json
import requests
import boto3
import os
import logging
from . import views
from .digitalocean import (
    get_droplets, 
    create_droplet, 
    start_droplet, 
    stop_droplet, 
    delete_droplet
)

# instantiate the Lambda client using boto3
lambda_client = boto3.client('lambda')

API_KEY = os.environ['API_KEY']

# setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Extract the operation from the event
        operation = event['operation']

        # Define operations mapping
        operations = {
            'load_template': views.load_template,
            'serve_page': views.serve_page,
            'get_interactions': views.get_interactions,
            'render_elements': views.render_elements,
            'handle_function': views.handle_function,
            'get_droplets': get_droplets,
            'create_droplet': create_droplet,
            'start_droplet': start_droplet,
            'stop_droplet': stop_droplet,
            'delete_droplet': delete_droplet,
        }

        # Validate operation is allowed
        if operation not in operations:
            raise ValueError(f'Invalid operation: {operation}')

        # Get the function to call
        func = operations[operation]

        # Get arguments for the function
        args = event.get('args', [])
        kwargs = event.get('kwargs', {})

        # Call the function with arguments
        result = func(*args, **kwargs)

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    except Exception as e:
        logger.error('An error occurred: %s', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }