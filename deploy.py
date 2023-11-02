```python
import os
import boto3
import subprocess
from botocore.exceptions import NoCredentialsError

# AWS region
AWS_REGION = os.environ.get('AWS_REGION')

# Function for installing Elastic Beanstalk CLI
def install_ebcli():
    """Installs the Elastic Beanstalk Command Line Interface on the local machine."""
    subprocess.run(['pip', 'install', 'awsebcli', '--upgrade', '--user'])

# Function for initializing an Elastic Beanstalk environment
def init_eb_environment():
    """Initializes an Elastic Beanstalk environment in the current directory."""
    # Note: This needs additional user input that can't be automated, such as region selection
    subprocess.run(['eb', 'init'])

# Function for creating Dockerrun.aws.json file
def create_dockerrun():
    """Creates a Dockerrun.aws.json file for Elastic Beanstalk to understand 
    how to deploy Docker container."""
    
    dockerrun_content = """
    {
        "AWSEBDockerrunVersion": "1",
        "Ports": [
            {
                "ContainerPort": "8000"
            }
        ],
        "Volumes": [],
        "Logging": "/var/log/nginx"
    }
    """
    
    with open('Dockerrun.aws.json', 'w') as file:
        file.write(dockerrun_content)

# Function for deploying application to Elastic Beanstalk
def eb_deploy():
    """Deploys the application to the Elastic Beanstalk environment."""
    subprocess.run(['eb', 'create'])

# Modified Function for creating lambda deployment zip
def prepare_deployment_zip():
    """Creates a .zip file containing Dockerrun.aws.json and Dockerfile."""
    with zipfile.ZipFile('eb_deployment.zip', 'w') as zipObj:
        zipObj.write('Dockerrun.aws.json') # including Dockerrun.aws.json file created above
        zipObj.write('Dockerfile') # assuming you have a Dockerfile in the same directory
    

def deploy():
    install_ebcli()
    init_eb_environment()
    create_dockerrun()
    eb_deploy()
    
if __name__ == '__main__':
    deploy()
```
Please note, this code assumes that you are running the script from the directory where your project is located. Also, user input is needed when running `eb init` command. This can't be automated in a Python script.