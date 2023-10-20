import requests
import json

def get_droplets(api_key):
    """
    Function to fetch droplet details from the DigitalOcean API.

    Args:
        api_key (str): The API key for authorization.

    Returns:
        list|None: List of droplets if successful. None if unsuccessful.
    """
    headers = {
        'Authorization': f'Bearer {dop_v1_19b5e565d434cd27716aebb89e2f4f2d2ae90d9ef5b9f48616cfff819d8ec950}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)
        response.raise_for_status()

        droplets = json.loads(response.text)['droplets']
        
        return droplets

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}. Error Code: {response.status_code}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    
    return None