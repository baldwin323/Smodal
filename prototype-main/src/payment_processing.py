```python
import requests
from src.config import APP_CONFIG
from src.exceptions import PaymentProcessingError

API_KEYS = APP_CONFIG['API_KEYS']
PAYMENT_GATEWAY_API_KEY = API_KEYS['PAYMENT_GATEWAY_API_KEY']
PAYMENT_GATEWAY_URL = APP_CONFIG['PAYMENT_GATEWAY_URL']

def process_payment(user_id, amount):
    payload = {
        'api_key': PAYMENT_GATEWAY_API_KEY,
        'user_id': user_id,
        'amount': amount
    }

    response = requests.post(PAYMENT_GATEWAY_URL, data=payload)

    if response.status_code != 200:
        raise PaymentProcessingError('Payment processing failed')

    return response.json()['transaction_id']

def refund_payment(transaction_id):
    payload = {
        'api_key': PAYMENT_GATEWAY_API_KEY,
        'transaction_id': transaction_id
    }

    response = requests.post(f"{PAYMENT_GATEWAY_URL}/refund", data=payload)

    if response.status_code != 200:
        raise PaymentProcessingError('Refund failed')

    return response.json()['refund_id']
```