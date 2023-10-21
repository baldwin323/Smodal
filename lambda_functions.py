import json
import requests
import boto3
import os
from . import views

# instantiate the Lambda client using boto3
lambda_client = boto3.client('lambda')

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