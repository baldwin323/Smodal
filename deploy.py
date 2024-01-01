```python
#!/usr/bin/env python3

import os
import subprocess
import shutil
from ai_config import docker, Credentials

KINSTA_DEPLOYMENT_TOKEN = Credentials.API_KEY # Updated using new API Key

def check_for_unstaged_changes():
    result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    if result.stdout:
        print("Unstaged changes detected. Please commit them before deploying.")
        exit(1)

def install_foreman():
    # We'll be using Foreman to run our combined Procfile
    if shutil.which("foreman") is None:
        print("Foreman not found. Installing now.")
        subprocess.run('gem install foreman'.split())
    print("Foreman is installed.")

def pull_app():
    subprocess.run('appservices pull --remote=data-evpxv mv data/* . && rm -r data'.split())

def git_add_commit_push():
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Update and build application'])
    subprocess.run(['git', 'push', 'origin', 'master'])

def create_workflow_file():   
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

def run_foreman():
    # Run foreman to start all processes defined in the Procfile
    subprocess.run('foreman start'.split())

def main():
    check_for_unstaged_changes()
    install_foreman() 
    pull_app()
    git_add_commit_push()
    create_workflow_file()
    run_foreman()

if __name__ == '__main__':
    main()
```
