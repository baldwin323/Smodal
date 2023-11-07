
```python
import boto3
import os
import subprocess

# AWS region
AWS_REGION = os.environ.get('AWS_REGION')

def install_docker():
    """Install Docker on the local machine."""
    subprocess.run(['curl', '-fsSL', 'https://get.docker.com', '|', 'sh'])

def install_ebcli():
    """Installs the Elastic Beanstalk Command Line Interface on the local machine."""
    subprocess.run(['pip', 'install', 'awsebcli', '--upgrade', '--user'])

def init_eb_environment():
    """Initializes an Elastic Beanstalk environment in the current directory."""
    subprocess.run(['eb', 'init'])
    
def build_docker_image():
    """Builds docker image using the Dockerfile in the current directory"""
    subprocess.run(['docker', 'build', '-t', 'my-image', '.'])
    
def push_to_ecr(repository_name, tag):
    """Pushes docker image to ECR"""
    repository_uri = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{repository_name}:{tag}"
    subprocess.run(['docker', 'push', repository_uri])

def configure_security_groups(sg_name):
    """Configures the security groups in AWS to allow inbound connections on the exposed ports"""
    ec2 = boto3.resource('ec2')
    security_group = ec2.SecurityGroup(sg_name)

    # Allow inbound connections on port 80
    security_group.authorize_ingress(
        IpProtocol="tcp",
        CidrIp="0.0.0.0/0",
        FromPort=80,
        ToPort=80,
    )
    
    # Allow inbound connections on port 443
    security_group.authorize_ingress(
        IpProtocol="tcp",
        CidrIp="0.0.0.0/0",
        FromPort=443,
        ToPort=443,
    )

def create_dockerrun():
    """Creates a Dockerrun.aws.json file for Elastic Beanstalk to understand 
    how to deploy Docker container.

    This configuration file is based on AWS Elastic Beanstalk multi-container Docker platform,
    and it describes how to deploy a Docker container from a Dockerfile in your source bundle."""
    
    dockerrun_content = """
    {
        "AWSEBDockerrunVersion": "1",
        "Image": {
            "Name": "your Docker Hub account/image-name",
            "Update": "true"
        },
        "Ports": [
            {
                "ContainerPort": "8000",
                "HostPort": "80"
            }
        ],
        "Volumes": [],
        "Logging": "/var/log/nginx",
        "environment": {
            "AWS_ACCESS_KEY": "your AWS access key",
            "AWS_SECRET_KEY": "your AWS secret key"
        }
    }
    """
    
    with open('Dockerrun.aws.json', 'w') as file:
        file.write(dockerrun_content)

def eb_deploy():
    """Deploys the application to the Elastic Beanstalk environment."""
    subprocess.run(['eb', 'deploy'])

def main():
    install_docker()
    install_ebcli()
    init_eb_environment()
    build_docker_image()
    push_to_ecr("your-ecr-repo", "latest")
    configure_security_groups("your-security-group")
    create_dockerrun()
    eb_deploy()

if __name__ == '__main__':
    main()
```
# This script now builds a Docker image, pushes it to Amazon ECR,
# configures security groups to allow inbound connections on the exposed ports,
# and triggers an AWS Elastic Beanstalk deployment.