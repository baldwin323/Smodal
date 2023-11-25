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

def build_angular_app():
    """Builds the Angular application"""
    # Specifies that we want Angular build to be production-ready
    subprocess.run('npm run build --prod'.split())


def git_add_commit_push():
    """Adds, commits, and pushes changes"""
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Update and build application'])
    subprocess.run(['git', 'push', 'origin', 'master'])


def build_docker_image():
    """Builds Docker image using Dockerfile in current directory"""
    # Docker compose build is used instead of docker build to ensure all services defined in docker-compose.yml are built.
    subprocess.run(['docker-compose', 'build'])


def run_docker_compose():
    """Starts the application using Docker Compose"""
    # This will start all services defined in the docker-compose.yml file, in the correct order.
    subprocess.run(['docker-compose', 'up', '-d'])


def main():
    check_for_unstaged_changes()
    pull_app()
    build_angular_app()   # Building Angular application
    git_add_commit_push()
    build_docker_image()
    run_docker_compose()


if __name__ == '__main__':
    main()
```
# The source code has been modified as follows:
# 1. A function to build the Angular application has been added. This builds the Angular app using the Angular CLI in prod mode.
# 2. The build_angular_app function is called in the main script right after the pull_app function. This ensures that any changes are built before they are committed and pushed to the git repo.
# 3. The commit message in the git_add_commit_push function has been updated to "Update and build application" to reflect the building of the Angular app.
# 4. All other functions are left as in the original code.