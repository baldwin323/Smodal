```python
import requests
from flask import Flask, request, jsonify
from src.config import APP_CONFIG

app = Flask(__name__)

@app.route('/connect-social-media', methods=['POST'])
def connect_to_social_media():
    user_data = request.get_json()
    social_media_platform = user_data.get('platform')

    if social_media_platform not in APP_CONFIG['SOCIAL_MEDIA_PLATFORMS']:
        return jsonify({'error': 'Invalid social media platform'}), 400

    api_key = APP_CONFIG['API_KEYS'][social_media_platform]

    response = requests.post(
        f"https://{social_media_platform}.com/oauth2/token",
        data={
            'grant_type': 'client_credentials',
            'client_id': api_key['client_id'],
            'client_secret': api_key['client_secret'],
            'scope': 'public'
        }
    )

    if response.status_code != 200:
        return jsonify({'error': 'Failed to connect to social media platform'}), 500

    access_token = response.json().get('access_token')
    return jsonify({'access_token': access_token}), 200
```