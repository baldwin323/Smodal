```python
#!/usr/bin/env python3

import os
import subprocess
import shutil
import pathlib
from ai_config import docker, Credentials

KINSTA_DEPLOYMENT_TOKEN = Credentials.API_KEY # Updated using new API Key

def check_for_unstaged_changes():
    result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    if result.stdout:
        print("Unstaged changes detected. Please commit them before deploying.")
        exit(1)

def check_and_install_docker_compose():
    if shutil.which("docker-compose") is None:
        print("docker-compose not found. Installing now.")
        subprocess.run('apt-get update'.split())
        subprocess.run('apt-get install docker-compose'.split())
    print("docker-compose is installed.")

def pull_app():
    subprocess.run('appservices pull --remote=data-evpxv mv data/* . && rm -r data'.split())

def build_angular_app():
    subprocess.run('npm run build --omit=dev'.split())

def git_add_commit_push():
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Update and build application'])
    subprocess.run(['git', 'push', 'origin', 'master'])

def create_workflow_file():
    # Create a workflow file for a Github action that deploys the app using Kinsta Deployment
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

# Includes procfile from 'prototype-main' directory.
def include_procfile_from_prototype_main():
    procfile_src = pathlib.Path("prototype-main/Procfile")
    procfile_dst = pathlib.Path("Procfile")
    shutil.copy(procfile_src, procfile_dst)

def build_docker_image():
    subprocess.run([docker, 'build', '-t', 'myapp', '.'])

def push_docker_image():
    subprocess.run([docker, 'push', 'myapp:latest'])

def run_docker_compose():
    subprocess.run([docker, 'compose', 'up', '-d'])

def start_frontend_from_prototype_main():
    old_cwd = os.getcwd()
    os.chdir("prototype-main")
    build_angular_app()
    os.chdir(old_cwd)

def main():
    check_for_unstaged_changes()
    check_and_install_docker_compose() 
    pull_app()
    start_frontend_from_prototype_main()
    include_procfile_from_prototype_main()
    create_workflow_file()
    git_add_commit_push()
    build_docker_image()
    push_docker_image()
    run_docker_compose()

if __name__ == '__main__':
    main()
```
