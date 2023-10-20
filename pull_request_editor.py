import os
from typing import List, Optional
from Smodal import logging  
from github import Github
from github.GithubException import RateLimitExceededException, BadCredentialsException

# ACCESS_TOKEN is used for OAuth authentication in GitHub API
ACCESS_TOKEN: str = os.getenv('GITHUB_ACCESS_TOKEN')

# Github instance using ACCESS_TOKEN
g = Github(ACCESS_TOKEN)

# Centralized logger for logging all the errors and information
logger = logging.getLogger(__name__)  

def get_open_pull_requests(repo_owner: str, 
                           repo_name: str
                           ) -> Optional[List[dict]]:
    """
    Function to fetch open pull requests from a repo.
    
    :param repo_owner: Name of the owner of the repository.
    :param repo_name: Name of the repository.
    
    :return: A list of dictionaries containing details of open pull requests. 
             If there's any error, it returns None
    """
    try:
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        open_pull_requests = repo.get_pulls(state = 'open')
        return open_pull_requests
    except RateLimitExceededException as e:
        logger.error(f'Rate limit exceeded while getting open pull requests: {str(e)}')
        raise e  
    except BadCredentialsException as e:
        logger.error(f'Bad credentials while getting open pull requests: {str(e)}')
        raise e 
    except Exception as e:
        logger.error(f'Unexpected error occurred while getting open pull requests: {str(e)}')
        raise e  

def edit_pull_request(repo_owner: str, 
                      repo_name: str, 
                      pull_id: int, 
                      title: str, 
                      body: str
                      ) -> bool:
    
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
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        pull_request = repo.get_pull(pull_id)
        pull_request.edit(title, body)
        return True
    except RateLimitExceededException as e:
        logger.error(f'Rate limit exceeded while editing pull request: {str(e)}')
        raise e  
    except BadCredentialsException as e:
        logger.error(f'Bad credentials while editing pull request: {str(e)}')
        raise e 
    except Exception as e:
        logger.error(f'Unexpected error occurred while editing pull request: {str(e)}')
        raise e  

def main() -> None:
    
    """
    Main function to get the open pull requests and edit them.
    """
    try:
        repo_owner: str = 'Smodal'
        repo_name: str = 'templates'

        open_pull_requests = get_open_pull_requests(repo_owner, repo_name)

        if open_pull_requests is None:
            return

        if open_pull_requests:   
            # your editing and other operation code here
            pass

    except RateLimitExceededException as e:
        logger.error(f'Rate limit exceeded in main function: {str(e)}')
    except BadCredentialsException as e:
        logger.error(f'Bad credentials occurred in main function: {str(e)}')
    except Exception as e:
        logger.error(f'Unexpected error occurred in main function: {str(e)}')