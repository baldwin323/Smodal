```python
import requests
from src.config import APP_CONFIG

API_KEYS = APP_CONFIG['API_KEYS']

def integrateAPI():
    social_media_api_key = API_KEYS['SOCIAL_MEDIA_API_KEY']
    payment_gateway_api_key = API_KEYS['PAYMENT_GATEWAY_API_KEY']

    social_media_api_url = 'https://api.socialmedia.com'
    payment_gateway_api_url = 'https://api.paymentgateway.com'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {social_media_api_key}'
    }

    response = requests.get(social_media_api_url, headers=headers)

    if response.status_code == 200:
        print('Successfully connected to social media API')

    headers['Authorization'] = f'Bearer {payment_gateway_api_key}'

    response = requests.get(payment_gateway_api_url, headers=headers)

    if response.status_code == 200:
        print('Successfully connected to payment gateway API')
```