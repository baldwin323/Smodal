import os
import requests
import logging

# Access token for GitHub API
ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

# Base URL for GitHub API
API_URL = 'https://api.github.com'

# Configuring logger for error tracking
logger=logging.getLogger()
logger.setLevel(logging.WARNING)

# Function to fetch open pull requests from a repo
def get_open_pull_requests(repo_owner, repo_name):
    # The url for getting pull requests of a Github repository
    url = f'{API_URL}/repos/{repo_owner}/{repo_name}/pulls'
    
    # headers needed for the api request
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    
    try:
        # Sending the request and gathering response 
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        logger.warning(f'Error occurred while getting pull requests: {str(e)}')
        return []
        
    # Returning the json response as a python list/dict    
    return response.json()

# Function that edits the title and description of a pull request
def edit_pull_request(repo_owner, repo_name, pull_id, title, body):
    # URL for the pull request to be edited
    url = f'{API_URL}/repos/{repo_owner}/{repo_name}/pulls/{pull_id}'

    # Header for the request to GitHub API
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    
    # Payload information to be updated
    payload = {'title': title, 'body': body}
    try: 
        # Making the PATCH request to GitHub API
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
    except Exception as e:
        logger.warning(f'Error occurred while editing pull request {pull_id}: {str(e)}')
        return None
    
    # Return the updated pull request's information
    return response.json()

# The main function
def main():
    repo_owner = 'Smodal'
    repo_name = 'templates'
    try:
        # Getting list of open pull requets
        open_pull_requests = get_open_pull_requests(repo_owner, repo_name)
    except Exception as e:
        logger.warning(f'Error occurred while getting open pull requests: {str(e)}')
        return

    # If there are open pull requests
    if open_pull_requests:    
        
        # Iterate over each pull request
        for pull_request in open_pull_requests:
            # The pull request id
            pull_id = pull_request['id']
            
            # New title and body for the pull request
            title = 'Modified title'
            body = 'Modified body'
            
            try:
                # Edit the pull request
                edited_pull_request = edit_pull_request(repo_owner, repo_name, pull_id, title, body)
                if edited_pull_request:
                    # Print success message after editing
                    print(f'Edited pull request {pull_id}.')
            except Exception as e:
                logger.warning(f'Error occurred while editing pull request {pull_id}: {str(e)}')

# Entry point of the Python script
if __name__ == "__main__":
    main()