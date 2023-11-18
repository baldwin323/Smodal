# Updated the python interpreter to python 3.12
# Ensured the requests library is compatible with python 3.12

# Importing necessary libraries
import requests
import json

# Retrieving droplets from DigitalOcean
def get_droplets(api_key):
    # Headers including API key for authorization
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    # Requesting data from the DigitalOcean API
    response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)

    # If the response is successful, return the list of droplets
    if response.status_code == 200:
        droplets = json.loads(response.text)['droplets']
        return droplets
    # If the response isn't successful, print the error and return None
    else:
        print(f"Error: {response.status_code}")
        return None
