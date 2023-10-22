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

# These are the new functions for handling affiliate manager operations
def register_affiliate_manager(event, context):
    # Logic for registering affiliate manager goes here
    pass


def monitor_affiliated_models(event, context):
    # Logic for monitoring affiliated models goes here
    pass


def give_credit(event, context):
    # Logic for giving credit when a new model signs up goes here
    pass


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
            'register_affiliate_manager': register_affiliate_manager,
            'monitor_affiliated_models': monitor_affiliated_models,
            'give_credit': give_credit,
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