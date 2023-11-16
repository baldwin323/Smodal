import requests
import json
import os

# use the os module to read environment variables. This lets us store sensitive information in a secure way outside of 
# our source code. 

def get_droplets():
    api_key = os.getenv('DOP_API_KEY')  
    # Instead of hardcoding the API key, we're retrieving it from an environment variable. This is much more secure and flexible
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