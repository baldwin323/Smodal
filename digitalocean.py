import requests
import json

def get_droplets(api_key):
    """
    Function to obtain the droplets from DigitalOcean's API.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',  # Use the passed API key for authorization
        'Content-Type': 'application/json',
    }

    try:
        # Make a GET request to the DigitalOcean API
        response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)

        # If the response status code is 200, it means the request was successful
        if response.status_code == 200:
            droplets = json.loads(response.text)['droplets']
            return droplets
        else:
            print(f"Error: {response.status_code}")
            return None

    except requests.ConnectionError as error:  # Catch any connection errors
        print(f'An error occurred: {error}')
        return None

    except Exception as error:  # Catch all other exceptions/errors
        print(f'An error occurred: {error}')
        return None
