import json
import requests
import boto3
import os
from . import views
from .digitalocean import get_droplets, create_droplet, start_droplet, stop_droplet, delete_droplet

# instantiate the Lambda client using boto3
lambda_client = boto3.client('lambda')

API_KEY = os.environ['API_KEY']

def lambda_handler(event, context):
    try:
        # Extract the operation from the event
        operation = event['operation']
        if operation == 'load_template':
            template_name = event['template_name']
            return views.load_template(template_name)
        elif operation == 'serve_page':
            request = event['request']
            page = event['page']
            return views.serve_page(request, page)
        elif operation == 'get_interactions':
            return views.get_interactions()
        elif operation == 'render_elements':
            request = event['request']
            page = event['page']
            return views.render_elements(request, page)
        elif operation == 'handle_function':
            function_name = event['function_name']
            args = event.get('args', [])
            kwargs = event.get('kwargs', {})
            return views.handle_function(function_name, *args, **kwargs)
        
        elif operation == 'get_droplets':
            return get_droplets(API_KEY)
        
        elif operation == 'create_droplet':
            size = event['size']
            image = event['image']
            region = event['region']
            return create_droplet(API_KEY, size, image, region)
        
        elif operation == 'start_droplet':
            droplet_id = event['droplet_id']
            return start_droplet(API_KEY, droplet_id)
        
        elif operation == 'stop_droplet':
            droplet_id = event['droplet_id']
            return stop_droplet(API_KEY, droplet_id)
        
        elif operation == 'delete_droplet':
            droplet_id = event['droplet_id']
            return delete_droplet(API_KEY, droplet_id)

        else:
            return {
                'statusCode': 400,
                'body': json.dumps(f'Invalid operation: {operation}')
            }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }