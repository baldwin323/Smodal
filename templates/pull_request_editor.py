import os
import requests
import logging

ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
API_URL = 'https://api.github.com'

# define a logger for error tracking
logger=logging.getLogger()
logger.setLevel(logging.WARNING)

def get_open_pull_requests(repo_owner, repo_name):
    url = f'{API_URL}/repos/{repo_owner}/{repo_name}/pulls'
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    try: 
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        logger.warning(f'Error occurred while getting pull requests: {str(e)}')
        return []
        
    return response.json()

def edit_pull_request(repo_owner, repo_name, pull_id, title, body):
    url = f'{API_URL}/repos/{repo_owner}/{repo_name}/pulls/{pull_id}'
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    payload = {'title': title, 'body': body}
    try: 
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
    except Exception as e:
        logger.warning(f'Error occurred while editing pull request {pull_id}: {str(e)}')
        return None
    
    return response.json()

def main():
    repo_owner = 'Smodal'
    repo_name = 'templates'
    try:
        open_pull_requests = get_open_pull_requests(repo_owner, repo_name)
    except Exception as e:
        logger.warning(f'Error occurred while getting open pull requests: {str(e)}')
        return

    if open_pull_requests:    
        for pull_request in open_pull_requests:
            pull_id = pull_request['id']
            title = 'Modified title'
            body = 'Modified body'
            try:
                edited_pull_request = edit_pull_request(repo_owner, repo_name, pull_id, title, body)
                if edited_pull_request:
                    print(f'Edited pull request {pull_id}.')
            except Exception as e:
                logger.warning(f'Error occurred while editing pull request {pull_id}: {str(e)}')

if __name__ == "__main__":
    main()