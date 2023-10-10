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

def create_droplet(api_key, name, region, size, image):
    data = {
        "name": name,
        "region": region,
        "size": size,
        "image": image
    }

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    response = requests.post('https://api.digitalocean.com/v2/droplets', headers=headers, json=data)

    if response.status_code == 202:
        return json.loads(response.text)
    else:
        print(f"Error: {response.status_code}")
        return None

# replace 'API_KEY', 'my-droplet-name', 'nyc1', 's-1vcpu-1gb', 'ubuntu-16-04-x64' with actual parameters
new_droplet = create_droplet('API_KEY', 'my-droplet-name', 'nyc1', 's-1vcpu-1gb', 'ubuntu-16-04-x64')