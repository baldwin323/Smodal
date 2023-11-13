
```python
import os
import subprocess

# Docker image and Vultr server IP
DOCKER_IMAGE = 'your-image-name'
VULTR_SERVER_IP = os.environ.get('VULTR_SERVER_IP')

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

def install_docker():
    """Install Docker on the local machine."""
    subprocess.run(['curl', '-fsSL', 'https://get.docker.com', '|', 'sh'])

def build_docker_image():
    """Builds Docker image using Dockerfile in current directory"""
    subprocess.run(['docker', 'build', '-t', DOCKER_IMAGE, '.'])
    
def push_to_docker_hub():
    """Push Docker image to Docker Hub"""
    subprocess.run(['docker', 'push', DOCKER_IMAGE])

def ssh_and_install_docker_on_vultr():
    """SSH to Vultr instance and install Docker."""
    subprocess.run(['ssh', VULTR_SERVER_IP, 'curl -fsSL https://get.docker.com | sh'])

def ssh_and_pull_docker_image_on_vultr():
    """SSH to Vultr instance and pull Docker image from Docker Hub."""
    subprocess.run(['ssh', VULTR_SERVER_IP, f'docker pull {DOCKER_IMAGE}'])

def ssh_and_run_docker_image_on_vultr():
    """SSH to Vultr instance and run Docker image, exposing required ports."""
    subprocess.run(['ssh', VULTR_SERVER_IP, f'docker run -p 8000:80 {DOCKER_IMAGE}'])

def main():
    check_for_unstaged_changes()
    pull_app()
    git_add_commit_push()
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
# 1. Added two new functions "pull_app" and "git_add_commit_push". "pull_app" function is used to pull data from a 
#    specific remote and copy it to local directory. Later it removes the 'data' directory. "git_add_commit_push" function 
#    is used to add all the changes to git, commit the changes and then push it to the master branch.
# 2. Included these functions in the main method to ensure they are executed when the script is run.
# 3. Original source code comments have been left untouched as they are still relevant to the new code.