import os
import requests
from typing import List, Optional
from Smodal import logging  

# ACCESS_TOKEN is used for OAuth authentication in GitHub API
ACCESS_TOKEN: str = os.getenv('GITHUB_ACCESS_TOKEN')

API_URL: str = 'https://api.github.com'  # base url of GitHub API

# centralized logger for logging all the errors and information
logger = logging.getLogger(__name__)  

def get_open_pull_requests(repo_owner: str, repo_name: str) -> Optional[List[dict]]:
    """
    Function to fetch open pull requests from a repo.
    
    :param repo_owner: Name of the owner of the repository.
    :param repo_name: Name of the repository.
    
    :return: A list of dictionaries containing details of open pull requests. 
    If there's any error, it returns None
    """
    try:
        # ... (code omitted for brevity)
    except Exception as e:
        logger.error(f'Error occurred while getting open pull requests: {str(e)}')
        # Raise the error for further handling
        raise e  

def edit_pull_request(repo_owner: str, repo_name: str, pull_id: int, title: str, body: str) -> bool:
    """
    Function to edit the title and description of a pull request.

    :param repo_owner: Name of the owner of the repository.
    :param repo_name: Name of the repository.
    :param pull_id: Pull request id.
    :param title: New title of the pull request.
    :param body: New description of the pull request.

    :return: True if the pull request was edited successfully, else False.
    """
    try:
        # ... (code omitted for brevity)
    except Exception as e:
        logger.error(f'Error occurred while editing pull request: {str(e)}')
        # Raise the error for further handling
        raise e  

def main() -> None:
    """
    Main function to get the open pull requests and edit them.
    """
    try:
        repo_owner: str = 'Smodal'
        repo_name: str = 'templates'
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