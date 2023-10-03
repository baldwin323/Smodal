import os
import requests
from Smodal import logging  # Importing the centralized logging instance

# Access token for GitHub API
ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

# Base URL for GitHub API
API_URL = 'https://api.github.com'

# Configuring logger for error tracking
logger = logging.getLogger(__name__)  # Replaced the standalone logger instance with the centralized logger instance

# Function to fetch open pull requests from a repo
def get_open_pull_requests(repo_owner, repo_name):
    # ... (code omitted for brevity)

# Function that edits the title and description of a pull request
def edit_pull_request(repo_owner, repo_name, pull_id, title, body):
    # ... (code omitted for brevity)

# The main function
def main():
    repo_owner = 'Smodal'
    repo_name = 'templates'
    try:
        # ... (code omitted for brevity)

        if open_pull_requests is None:
            return
    except Exception as e:
        logger.warning(f'Error occurred while getting open pull requests: {str(e)}')  # Utilizing the centralized logger instance here
        return

    # If there are open pull requests
    if open_pull_requests:   
        # ... (code omitted for brevity)