import requests
import json

def get_droplets(api_key):
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

def create_droplet(api_key, size, image, region):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        "name": "sample_droplet",
        "region": region,
        "size": size,
        "image": image,
    }
    response = requests.post('https://api.digitalocean.com/v2/droplets', headers=headers, json=data)

def start_droplet(api_key, droplet_id):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    response = requests.post(f'https://api.digitalocean.com/v2/droplets/{droplet_id}/actions', headers=headers, json={"type": "power_on"})

def stop_droplet(api_key, droplet_id):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    response = requests.post(f'https://api.digitalocean.com/v2/droplets/{droplet_id}/actions', headers=headers, json={"type": "power_off"})

def delete_droplet(api_key, droplet_id):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    response = requests.delete(f'https://api.digitalocean.com/v2/droplets/{droplet_id}', headers=headers)