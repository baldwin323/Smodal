```python
import requests
from src.config import APP_CONFIG
from src.exceptions import NetworkError

def networkClonedUser(user_id, clone_id):
    try:
        # Get the API keys from the APP_CONFIG
        social_media_api_key = APP_CONFIG['SOCIAL_MEDIA_API_KEY']
        payment_gateway_api_key = APP_CONFIG['PAYMENT_GATEWAY_API_KEY']

        # Prepare the headers for the requests
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {social_media_api_key}:{payment_gateway_api_key}'
        }

        # Prepare the payload for the requests
        payload = {
            'user_id': user_id,
            'clone_id': clone_id
        }

        # Send a POST request to the social media API
        social_media_response = requests.post(
            f'{APP_CONFIG["SOCIAL_MEDIA_API_URL"]}/network',
            headers=headers,
            json=payload
        )

        # Check if the request was successful
        if social_media_response.status_code != 200:
            raise NetworkError('Failed to network the cloned user on social media')

        # Send a POST request to the payment gateway API
        payment_gateway_response = requests.post(
            f'{APP_CONFIG["PAYMENT_GATEWAY_API_URL"]}/network',
            headers=headers,
            json=payload
        )

        # Check if the request was successful
        if payment_gateway_response.status_code != 200:
            raise NetworkError('Failed to network the cloned user on the payment gateway')

        return True

    except Exception as e:
        raise NetworkError(str(e))
```