import requests
import json

def get_droplets(api_key):
    headers = {
        'Authorization': f'Bearer {dop_v1_19b5e565d434cd27716aebb89e2f4f2d2ae90d9ef5b9f48616cfff819d8ec950}',
        'Content-Type': 'application/json',
    }

    response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)

    if response.status_code == 200:
        droplets = json.loads(response.text)['droplets']
        return droplets
    else:
        print(f"Error: {response.status_code}")
        return None