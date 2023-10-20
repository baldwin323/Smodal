import requests
import logging
import json

logging.basicConfig(level=logging.INFO)

def get_droplets(api_key):
    """
    Function to fetch droplet details from the DigitalOcean API.

    Args:
        api_key (str): The API key for authorization.

    Returns:
        list|None: List of droplets if successful. None if unsuccessful.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)
        response.raise_for_status()

        droplets = json.loads(response.text)['droplets']
        
        return droplets

    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}, Error Code: {response.status_code}')
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
    
    return None