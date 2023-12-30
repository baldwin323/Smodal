```python
#!/usr/bin/env python3
# Ensure the shebang line at the top of the deploy.py script specifies the correct interpreter. 
# It is recommended to use "/usr/bin/env python3" which will work for virtually all systems where python3 is installed.

import os
import subprocess
import shutil

# Imported docker from ai_config.py
from ai_config import docker, Credentials

# Updated KINSTA_DEPLOYMENT_TOKEN using new API Key
KINSTA_DEPLOYMENT_TOKEN = Credentials.API_KEY

def check_for_unstaged_changes():
    """Check if there are any unstaged changes in the git repo"""
    result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    if result.stdout:
        print("Unstaged changes detected. Please commit them before deploying.")
        exit(1)

def check_and_install_docker_compose():
    """Checks if docker-compose is installed and if not, installs it"""
    # This is a new function to ensure docker-compose is existing in the system before proceed forward. 
    if shutil.which("docker-compose") is None:
        print("docker-compose not found. Installing now.")
        subprocess.run('apt-get update'.split())
        subprocess.run('apt-get install docker-compose'.split())
    print("docker-compose is installed.")

def pull_app():
    """Pulls data from remote"""
    subprocess.run('appservices pull --remote=data-evpxv mv data/* . && rm -r data'.split())

def build_angular_app():
    """Builds the Angular application"""
    subprocess.run('npm run build --omit=dev'.split())

def git_add_commit_push():
    """Adds, commits, and pushes changes"""
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Update and build application'])
    subprocess.run(['git', 'push', 'origin', 'master'])

def create_workflow_file():
    """Creates a Github workflow file for the Kinsta deployment"""   
    workflow_content = f'''
name: Deploy App with Kinsta Deployment
on:   
  push:     
    branches: ["main"]
  workflow_dispatch:  
permissions:   
  contents: read   
  pages: write  
  secrets: write
concurrency:   
  group: "kinsta-deploy"   
  cancel-in-progress: false  
jobs:   
  deploy:     
    runs-on: ubuntu-latest  
    steps:       
      - name: Checkout         
        uses: actions/checkout@v2       
      - name: Setup Kinsta Deployment       
        uses: cicirello/kinsta-deployment@v2
        with:
          token: {KINSTA_DEPLOYMENT_TOKEN}
    '''
    with open('.github/workflows/deploy.yaml', 'w') as workflow_file:
        workflow_file.write(workflow_content)

def build_docker_image():
    """Builds Docker image using Dockerfile in current directory"""
    subprocess.run([docker, 'build', '-t', 'myapp', '.'])

def push_docker_image():
    """Push the Docker image to Docker Hub"""
    subprocess.run([docker, 'push', 'myapp:latest'])

def run_docker_compose():
    """Starts the application using Docker Compose"""
    subprocess.run([docker, 'compose', 'up', '-d'])

def main():
    check_for_unstaged_changes()
    check_and_install_docker_compose() 
    pull_app()
    build_angular_app()
    create_workflow_file()
    git_add_commit_push()
    build_docker_image()
    push_docker_image()
    run_docker_compose()

if __name__ == '__main__':
    main()
```
