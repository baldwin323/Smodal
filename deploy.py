
```python
import os
import subprocess

# Updated to include VULTR_SERVER_IP
VULTR_SERVER_IP = os.environ.get('VULTR_SERVER_IP')

# Docker image
DOCKER_IMAGE = 'your-image-name'

def install_docker():
    """Install Docker on the local machine."""
    subprocess.run(['curl', '-fsSL', 'https://get.docker.com', '|', 'sh'])

def build_docker_image():
    """Builds docker image using the Dockerfile in the current directory"""
    subprocess.run(['docker', 'build', '-t', DOCKER_IMAGE, '.'])
    
def push_to_docker_hub():
    """Pushes docker image to Docker Hub"""
    subprocess.run(['docker', 'push', DOCKER_IMAGE])

def ssh_and_install_docker_on_vultr():
    """SSH into the Vultr instance and install Docker."""
    subprocess.run(['ssh', VULTR_SERVER_IP, 'curl -fsSL https://get.docker.com | sh'])

def ssh_and_pull_docker_image_on_vultr():
    """SSH into the Vultr instance and pull Docker image from Docker Hub."""
    subprocess.run(['ssh', VULTR_SERVER_IP, f'docker pull {DOCKER_IMAGE}'])

def ssh_and_run_docker_image_on_vultr():
    """SSH into the Vultr instance and run Docker image, exposing required ports."""
    subprocess.run(['ssh', VULTR_SERVER_IP, f'docker run -p 8000:80 {DOCKER_IMAGE}'])

def main():
    install_docker()
    build_docker_image()
    push_to_docker_hub()
    ssh_and_install_docker_on_vultr()
    ssh_and_pull_docker_image_on_vultr()
    ssh_and_run_docker_image_on_vultr()

if __name__ == '__main__':
    main()
```

# Changes:
# 1. Replaced AWS Elastic Beanstalk deployment commands with Docker commands to pull and run the image on Vultr.
# 2. Added VULTR_SERVER_IP environment variable to take vultr instance IP from environment.
# 3. Added DOCKER_IMAGE constant to hold Docker image name.
# 4. Split the single AWS deployment step into:
#    a. Docker image building and pushing on local machine.
#    b. SSH into Vultr, installing Docker, pulling and running image.
# 5. Removed AWS related functions and configurations.
# 6. Script now pulls the Docker image from Docker Hub to the Vultr instance and runs it, exposing the required ports.
