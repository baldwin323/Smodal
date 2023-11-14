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
    subprocess.run(['git', 'commit', '-m', 'Update application'])
    subprocess.run(['git', 'push', 'origin', 'master'])


def build_docker_image():
    """Builds Docker image using Dockerfile in current directory"""
    # The docker-compose build command is used because it will automatically find and build images based on the services described in the docker-compose.yml file in the current directory.
    subprocess.run(['docker-compose', 'build'])

    
def run_docker_compose():
    """Starts the application using Docker Compose"""
    # This will start all services defined in the docker-compose.yml file, in the correct order.
    subprocess.run(['docker-compose', 'up', '-d'])


def main():
    check_for_unstaged_changes()
    pull_app()
    git_add_commit_push()
    build_docker_image()
    run_docker_compose()


if __name__ == '__main__':
    main()
```
# Modified the deploy.py file:
# 1. Added a function to build the Docker images based on docker-compose.yml.
# 2. Added a new function to start application using Docker Compose with a single command.
# 3. Modified the main function to run these two newly added functions.