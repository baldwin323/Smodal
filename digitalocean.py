import requests
import json
import os

def get_droplets():
    api_key = os.getenv('DO_API_KEY')

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)

    if response.status_code == 200:
        droplets = json.loads(response.text)['droplets']
        return droplets
    else:
        print(f"Error: {response.status_code}")
        return None