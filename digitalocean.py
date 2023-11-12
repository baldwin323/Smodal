import requests
import json
import os   # Added to import os module to read environment variable


def get_api_key():   # Function added to securely fetch API key from os environment variable
    """
    Function to securely fetch the API key from an environment variable.
    The name of the environment variable is 'DOP_API_KEY'
    """
    api_key = os.getenv('DOP_API_KEY')
    if api_key is None:
        raise ValueError('DOP_API_KEY not found in environment variables')
    return api_key
    

def get_droplets(api_key):
    headers = {
        'Authorization': f'Bearer {get_api_key()}',  # Updated to fetch the api_key using the new function
        'Content-Type': 'application/json',
    }

    try:   # Error Handling block added to handle exceptions during API Requests
        response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)
        response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None
    else:
        if response.status_code == 200:
            droplets = json.loads(response.text)['droplets']
            return droplets
        else:
            print(f"Error: {response.status_code}")
            return None
