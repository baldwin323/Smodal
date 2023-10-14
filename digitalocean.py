import requests
import json
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('digitalocean.log')
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

def get_droplets(api_key):
    headers = {
        'Authorization': f'Bearer {dop_v1_19b5e565d434cd27716aebb89e2f4f2d2ae90d9ef5b9f48616cfff819d8ec950}',
        'Content-Type': 'application/json',
    }

    response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)

    # Add additional checks for the status code
    if response.status_code == 200:
        droplets = json.loads(response.text)['droplets']
        return droplets
    elif response.status_code >= 400 and response.status_code < 500:
        logger.error(f"Client error: {response.status_code} {response.reason} {response.text}")
    elif response.status_code >= 500:
        logger.error(f"Server error: {response.status_code} {response.reason} {response.text}")
    else:
        logger.error(f"Unexpected status code: {response.status_code}")
    return None