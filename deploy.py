import os
import boto3
from botocore.exceptions import NoCredentialsError
from PyInstaller.__main__ import run as pyinstaller_run

# AWS region
AWS_REGION = os.environ.get('AWS_REGION')

# Function for creating executable and bundling dependencies
def prepare_executable():
    pyinstaller_run(['lambda_functions.py', '--onefile'])

# Function for creating lambda function
def create_lambda(func_name):
    # Create lambda client
    lambda_client = boto3.client('lambda', region_name=AWS_REGION)
    # Create lambda function
    lambda_client.create_function(
        FunctionName=func_name,
        Runtime='python3.8',
        Role='lambda-basic-execution',
        Handler='lambda_handler.lambda_handler',
        Code={'ZipFile': open('dist/lambda_functions', 'rb').read()},
        Description='Lambda function for managing DigitalOcean droplets',
        Timeout=15,
        MemorySize=128
    )

# Function for creating API Gateway event trigger
def create_gateway_trigger():
    # Create API Gateway client
    gateway_client = boto3.client('apigateway', region_name=AWS_REGION)
    # Create REST API
    api = gateway_client.create_rest_api(
        name='ServerlessDropletAPI',
        description='API for serverless DigitalOcean droplets management'
    )
    # Create resources
    root_resource = gateway_client.get_resources(
        restApiId=api['id']
    )['items'][0]
    invoke_resource = gateway_client.create_resource(
        restApiId=api['id'],
        parentId=root_resource['id'],
        pathPart='invoke'
    )
    # Create method
    gateway_client.put_method(
        restApiId=api['id'],
        resourceId=invoke_resource['id'],
        httpMethod='POST',
        authorizationType='NONE'
    )
    # Create integration
    gateway_client.put_integration(
        restApiId=api['id'],
        resourceId=invoke_resource['id'],
        httpMethod='POST',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{AWS_REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:{AWS_REGION}:{os.environ.get("AWS_ACCOUNT_ID")}:function:serverless-modal-exec/invocations'
    )
    # Deploy API
    gateway_client.create_deployment(
        restApiId=api['id'],
        stageName='prod'
    )

# Function for creating S3 event trigger
def create_s3_trigger(bucket_name, func_name):
    # Create S3 client
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': AWS_REGION
            }
        )
        # Create S3 event trigger
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

# Main function for deployment
def deploy():
    func_name = 'serverless-droplet-manager'
    bucket_name = 'serverless-droplet-manager-bucket'
    prepare_executable()
    create_lambda(func_name)
    create_gateway_trigger()
    create_s3_trigger(bucket_name, func_name)
    
# Function for providing deployment instructions
def deployment_instructions():
    print("Deployment Instructions:")
    print("1. Ensure AWS credentials are configured correctly.")
    print("2. Run this script to create the lambda functions, API Gateway event trigger, and S3 event trigger.")
    print("3. After running the script, navigate over to AWS management console to verify that the actions have completed correctly.")
    print("4. Upon a successful run of the script, the react application is now ready to be deployed to the configured AWS services.")

if __name__ == '__main__':
    deploy()
    deployment_instructions()