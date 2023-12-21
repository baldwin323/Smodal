
```python
import os
import subprocess
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
    """Creates a Github workflow file for the Jekyll deployment"""  
    arcpy.AddMessage("Creating the Github workflow file for Kinsta deployment with updated API Key...")
    
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
    arcpy.AddMessage("Workflow file has been created successfully.")


def build_docker_image():
    """Builds Docker image using Dockerfile in current directory"""
    arcpy.AddMessage("Building the Docker image for the containerized application...")
    subprocess.run([docker, 'build', '.'])
    arcpy.AddMessage("Docker image has been built successfully.")


def run_docker_compose():
    """Starts the application using Docker Compose"""
    arcpy.AddMessage("Starting the app using Docker Compose...")
    subprocess.run([docker, 'compose', 'up', '-d'])
    arcpy.AddMessage("The application has been started successfully.")


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
# 1. Importing Docker and Credentials from ai_config.py to use Docker and the updated API Key.
# 2. Updating the Kinsta Deployment token in the KINSTA token variable to use the new API Key from Credentials.
# 3. Updating the build_angular_app function to exclude development dependencies.
# 4. Updating build_docker_image and run_docker_compose function to use Docker from ai_config.py
# 5. Adding relevant status messages within functions to denote progress.
# 6. Adding relevant comments to indicate the changes made.