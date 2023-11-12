import requests
import json
import os   # This module is required to read from environment variable

def get_api_key():
    """
    This function fetches the API key from an environment variable named 'DOP_API_KEY'.
    Raises a ValueError exception if the environment variable is not set up properly.
    """
    api_key = os.getenv('DOP_API_KEY')
    if api_key is None:
        raise ValueError('DOP_API_KEY not set in environment variables')
    return api_key

def get_droplets(api_key):
    """
    This function makes a GET request to the DigitalOcean API to fetch a list of droplets.
    It takes one argument, api_key which is the API Key for the DigitalOcean API.
    """

    # Headers for the API Request. 'Authorization' is Bearer Token composed of the api_key
    headers = {
        'Authorization': f'Bearer {get_api_key(api_key)}',
        'Content-Type': 'application/json',
    }

    # Error handling block to catch and handle exceptions during the API Request
    try:
        response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)
        response.raise_for_status()  # This will raise an HTTPError if the request returned an unsuccessful status code

    # Handle HTTPError exceptions
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None

    # Handle other exceptions
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None
    else:
        # Check if the status code of the response is 200 (Success)
        if response.status_code == 200:
            # Extract the 'droplets' field from the JSON response
            droplets = json.loads(response.text)['droplets']
            return droplets
        else:
            print(f"Error: {response.status_code}")
            return None