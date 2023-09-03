```python
import requests
import unittest
from unittest.mock import patch
from src.api_integration import integrateAPI

class TestApiIntegration(unittest.TestCase):

    @patch('src.api_integration.requests.get')
    def test_integrateAPI(self, mock_get):
        mock_get.return_value.status_code = 200

        social_media_api_result = integrateAPI('SOCIAL_MEDIA_API_KEY', 'https://api.socialmedia.com')
        payment_gateway_api_result = integrateAPI('PAYMENT_GATEWAY_API_KEY', 'https://api.paymentgateway.com')

        self.assertTrue(social_media_api_result, 'Successfully connected to social media API')
        self.assertTrue(payment_gateway_api_result, 'Successfully connected to payment gateway API')


if __name__ == '__main__':
    unittest.main()
```
Please note that the function integrateAPI() was slightly modified to take both api key and url as parameters for better testability. Kindly update the original script accordingly.