import requests
from requests.exceptions import RequestException
from flask import jsonify

class BankingAPI:
    def __init__(self, api_url, api_key):
        self.base_url = api_url
        self.api_key = api_key

    def authenticate(self):
        auth_url = f"{self.base_url}/auth"
        try:
            response = requests.post(auth_url, headers={'Authorization': self.api_key})
            response.raise_for_status()
            return True
        except RequestException as e:
            print(f"Error during authentication: {str(e)}")
            return False

    def make_request(self, endpoint, method="GET", data={}):
        url = f"{self.base_url}/{endpoint}"
        
        headers = {
            'Authorization': self.api_key,
        }
        
        try:
            if method == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                response = requests.get(url, headers=headers)

            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error with {method} request to {url}: {str(e)}")
            return None

banking_api = BankingAPI('https://fakeapi.com', 'your_api_key')

def authenticate_and_make_request(endpoint, method="GET", data={}):
    if not banking_api.authenticate():
        return jsonify({'error': 'Cannot authenticate with the banking API.'}), 500

    response = banking_api.make_request(endpoint, method, data)

    if response is None:
        return jsonify({'error': 'Unable to complete the request.'}), 500
        
    if 'error' in response:
        return jsonify({'error': response['error']}), 500
        
    return jsonify(response), 200