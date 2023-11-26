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
    """Pulls the latest version of the application from the repository"""
    subprocess.run('git pull origin master'.split())


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
    # Docker compose build is used instead of docker build to ensure all services
    # defined in docker-compose.yml are built.
    subprocess.run(['docker-compose', 'build'])

def run_docker_compose():
    """Starts the application using Docker Compose"""
    # This will start all services defined in the docker-compose.yml file, 
    # in the correct order.
    subprocess.run(['docker-compose', 'up', '-d'])

def generate_teamcity_build_configuration_template():
    """Generates a build configuration template for TeamCity deployment"""
    # The steps for the deployment process are defined here and are executed
    # in the order they are called.
    check_for_unstaged_changes()
    pull_app()
    build_angular_app()
    git_add_commit_push()
    build_docker_image()
    run_docker_compose()

def main():
    generate_teamcity_build_configuration_template()


if __name__ == '__main__':
    main()
```

