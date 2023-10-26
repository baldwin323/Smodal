import os
import shutil
import zipfile
import boto3
from botocore.exceptions import NoCredentialsError
from PyInstaller.__main__ import run as pyinstaller_run

# AWS region
AWS_REGION = os.environ.get('AWS_REGION')

# Function for creating executable and bundling dependencies
def prepare_executable():
    """Creates an executable from lambda_functions.py with all its dependencies bundled."""
    pyinstaller_run(['lambda_functions.py', '--onefile'])

# Modified Function for creating lambda deployment zip
def prepare_deployment_zip():
    """Creates a .zip file containing lambda_functions.py and its dependencies."""
    # Create a ZipFile Object and include the new lambda_functions.zip created by compress_directory() function in lambda_functions.py
    with zipfile.ZipFile('lambda_deployment.zip', 'w') as zipObj:
        # Add multiple files to the zip
        zipObj.write('lambda_functions.zip', arcname='lambda_functions.zip')
        zipObj.write('requirements.txt', arcname='requirements.txt')

# Function for creating lambda function
def create_lambda(func_name):
    """Creates a new lambda function with the given function name."""
    # Create lambda client
    lambda_client = boto3.client('lambda', region_name=AWS_REGION)
    # Create lambda function
    lambda_client.create_function(
        FunctionName=func_name,
        Runtime='python3.8',
        Role='lambda-basic-execution',
        Handler='lambda_handler.lambda_handler',
        # Changed Code parameter to upload a zip file instead of individual files.
        Code={'ZipFile': open('lambda_functions.zip', 'rb').read()},
        Description='Lambda function for managing DigitalOcean droplets',
        Timeout=15,
        MemorySize=128
    )

# Rest of the file remains the same as original code
def create_gateway_trigger():
    """Creates a new API Gateway event trigger."""
    gateway_client = boto3.client('apigateway', region_name=AWS_REGION)
    api = gateway_client.create_rest_api(
        name='ServerlessDropletAPI',
        description='API for serverless DigitalOcean droplets management'
    )
    root_resource = gateway_client.get_resources(
        restApiId=api['id']
    )['items'][0]
    invoke_resource = gateway_client.create_resource(
        restApiId=api['id'],
        parentId=root_resource['id'],
        pathPart='invoke'
    )
    gateway_client.put_method(
        restApiId=api['id'],
        resourceId=invoke_resource['id'],
        httpMethod='POST',
        authorizationType='NONE'
    )
    gateway_client.put_integration(
        restApiId=api['id'],
        resourceId=invoke_resource['id'],
        httpMethod='POST',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{AWS_REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:{AWS_REGION}:{os.environ.get("AWS_ACCOUNT_ID")}:function:serverless-modal-exec/invocations'
    )
    gateway_client.create_deployment(
        restApiId=api['id'],
        stageName='prod'
    )

def create_s3_trigger(bucket_name, func_name):
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': AWS_REGION
            }
        )
        lambda_client = boto3.client('lambda', region_name=AWS_REGION)
        lambda_client.create_event_source_mapping(
            EventSourceArn=f'arn:aws:s3:::{bucket_name}',
            FunctionName=func_name,
            Enabled=True,
            BatchSize=1,
            StartingPosition='TRIM_HORIZON'
        )
    except NoCredentialsError:
        print("No AWS credentials were found.")

def deploy():
    func_name = 'serverless-droplet-manager'
    bucket_name = 'serverless-droplet-manager-bucket'
    prepare_executable()
    prepare_deployment_zip()
    create_lambda(func_name)
    create_gateway_trigger()
    create_s3_trigger(bucket_name, func_name)

def deployment_instructions():
    print("Deployment Instructions:")
    print("1. Ensure AWS credentials are configured correctly.")
    print("2. Run this script to create the lambda functions, API Gateway event trigger, and S3 event trigger.")
    print("3. After running the script, navigate over to AWS management console to verify that the actions have completed correctly.")
    print("4. Make sure the S3 bucket created is correctly configured for static website hosting.")
    print("5. Upload the built application files to the newly created S3 bucket.")
    print("6. Use the files in the S3 bucket to serve the React application.")
    print("7. If necessary, configure a CDN or attach an existing one to the S3 bucket.")
    print("8. Now your React Frontend application is live on AWS.")

if __name__ == '__main__':
    deploy()
    deployment_instructions()