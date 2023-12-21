```python
import os
from ai_config import Credentials # Imported Credentials from ai_config.py
import subprocess

KINSTA_DEPLOYMENT_TOKEN = os.getenv("KINSTA_DEPLOYMENT_TOKEN")

def check_for_unstaged_changes():
    """Check if there are any unstaged changes in the git repo"""
    result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    if result.stdout:
        print("Unstaged changes detected. Please commit them before deploying.")
        exit(1)


def pull_app():
    """Pulls data from remote"""
    subprocess.run('appservices pull --remote=data-evpxv mv data/* . && rm -r data'.split())


def build_angular_app():
    """Builds the Angular application"""
    # Specifies that we want Angular build to be production-ready
    subprocess.run('npm run build --prod'.split())


def git_add_commit_push():
    """Adds, commits, and pushes changes"""
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Update and build application'])
    subprocess.run(['git', 'push', 'origin', 'master'])


def create_workflow_file():
    """Creates a Github workflow file for the Jekyll deployment"""  
    # Integrated new API credentials for Kinsta Deployment
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
          token: {Credentials.API_KEY}  # Updated API Key from ai_config.py
    '''
    with open('.github/workflows/deploy.yaml', 'w') as workflow_file:
        workflow_file.write(workflow_content)


def build_docker_image():
    """Builds Docker image using Dockerfile in current directory"""
    subprocess.run(['docker', 'build', '.'])


def run_docker_compose():
    """Starts the application using Docker Compose"""
    subprocess.run(['docker-compose', 'up', '-d'])


def main():
    check_for_unstaged_changes()
    pull_app()
    build_angular_app()
    create_workflow_file()  # Creating the GitHub workflow file for Kinsta deployment with updated API Key
    git_add_commit_push()
    build_docker_image()  # Build the Docker image for the containerized application
    run_docker_compose()  # Run the app using Docker Compose


if __name__ == '__main__':
    main()
```
# Changes to the source code include:
# 1. Importing Credentials from ai_config.py to use the updated API Key.
# 2. Updating the Kinsta Deployment token in the create_workflow_file() function to use the new API Key from Credentials.
# 3. Adding relevant comments to indicate the changes made.