import os
import requests
from Smodal import logging  

ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

API_URL = 'https://api.github.com'

logger = logging.getLogger(__name__)  # centralized logger

def get_open_pull_requests(repo_owner, repo_name):
    """
    Function to fetch open pull requests from a repo.
    """
    try:
        # ... (code omitted for brevity)
    except Exception as e:
        logger.error(f'Error occurred while getting open pull requests: {str(e)}')
        # Raise the error for further handling
        raise e  

def edit_pull_request(repo_owner, repo_name, pull_id, title, body):
    """
    Function that edits the title and description of a pull request.
    """
    try:
        # ... (code omitted for brevity)
    except Exception as e:
        logger.error(f'Error occurred while editing pull request: {str(e)}')
        # Raise the error for further handling
        raise e  

def main():
    try:
        repo_owner = 'Smodal'
        repo_name = 'templates'
        # ... (code omitted for brevity)

        if open_pull_requests is None:
            return
    except Exception as e:
        logger.error(f'Error occurred while getting open pull requests: {str(e)}')
        # Raise the error for further handling
        raise e  

    # If there are open pull requests
    if open_pull_requests:   
        # ... (code omitted for brevity)
