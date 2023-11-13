
```python
import os
import subprocess

def check_for_unstaged_changes():
    """Check if there are any unstaged changes in the git repo"""
    result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    if result.stdout:
        print("Unstaged changes detected. Please commit them before deploying.")
        exit(1)

def pull_app():
    """Pulls data from remote"""
    subprocess.run('appservices pull --remote=data-evpxv mv data/* . && rm -r data'.split())

def git_add_commit_push():
    """Adds, commits, and pushes changes"""
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit'])
    subprocess.run(['git', 'push', 'origin', 'master'])


def build_docker_image():
    """Builds Docker image using Dockerfile in current directory"""
    # We use "docker-compose build" for building the image
    subprocess.run(['docker-compose', 'build'])

def run_docker_compose():
    """Runs Docker Compose up, effectively launching the full application"""
    subprocess.run(['docker-compose', 'up'])

def main():
    check_for_unstaged_changes()
    pull_app()
    git_add_commit_push()
    build_docker_image()
    run_docker_compose()

if __name__ == '__main__':
    main()
```

# Changes:
# 1. Removed Vultr server and Docker hub related code as per the provided instructions.
# 2. Modified the build_docker_image function to build Docker image using docker-compose.
# 3. Added a new function run_docker_compose to run the Docker Compose up, which will start all the services specified in the docker-compose.yml file.
# 4. Modified the main function to incorporate the changes.
