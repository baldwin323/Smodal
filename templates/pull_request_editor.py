import os
import requests

ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
API_URL = 'https://api.github.com'

def get_open_pull_requests(repo_owner, repo_name):
    url = f'{API_URL}/repos/{repo_owner}/{repo_name}/pulls'
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def edit_pull_request(repo_owner, repo_name, pull_id, title, body):
    url = f'{API_URL}/repos/{repo_owner}/{repo_name}/pulls/{pull_id}'
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    payload = {'title': title, 'body': body}
    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    repo_owner = 'Smodal'
    repo_name = 'templates'
    open_pull_requests = get_open_pull_requests(repo_owner, repo_name)
    
    for pull_request in open_pull_requests:
        pull_id = pull_request['id']
        title = 'Modified title'
        body = 'Modified body'
        edited_pull_request = edit_pull_request(repo_owner, repo_name, pull_id, title, body)
        print(f'Edited pull request {pull_id}.')

if __name__ == "__main__":
    main()