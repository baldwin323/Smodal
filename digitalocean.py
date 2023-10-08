import requests
import json
import os
from typing import Union, List

def get_droplets() -> Union[List[dict], None]:
    """
    This function makes a GET request to the DigitalOcean API to retrieve a list of droplets.
    :return: List of droplets if the API call is successful; None otherwise
    """
    
    api_key = os.getenv('DO_API_KEY')
    
    if not api_key:
        print("Missing API key.")
        return None

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)

        if response.status_code == 200:
            droplets = json.loads(response.text)['droplets']
            return droplets
        else:
            print(f"Error: {response.status_code}")
            return None
    except (requests.RequestException, KeyError) as error:
        print(f"Error in get_droplets: {error}")
        return None