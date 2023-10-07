import requests
import json

def get_droplets(api_key):
    headers = {
        'Authorization': f'Bearer {dop_v1_f14e98d64199585c9df696e6b2e49cc574799438799600ec0ad8beda0d933281}',
        'Content-Type': 'application/json',
    }

    response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)

    if response.status_code == 200:
        droplets = json.loads(response.text)['droplets']
        return droplets
    else:
        print(f"Error: {response.status_code}")
        return None