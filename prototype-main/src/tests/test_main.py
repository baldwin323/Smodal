```python
import unittest
from unittest.mock import patch
from src.main import app
import json

class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        assert response.status_code == 200

    @patch('src.main.startCloneTraining')
    def test_clone_training(self, mock_startCloneTraining):
        mock_startCloneTraining.return_value = None
        response = self.app.post('/start-clone-training', data=json.dumps({'user_data': 'test'}), content_type='application/json')
        assert response.status_code == 200

    @patch('src.main.connectToSocialMedia')
    def test_social_media_connect(self, mock_connectToSocialMedia):
        mock_connectToSocialMedia.return_value = None
        response = self.app.post('/connect-social-media', data=json.dumps({'user_data': 'test'}), content_type='application/json')
        assert response.status_code == 200

    @patch('src.main.processPayment')
    def test_payment_processing(self, mock_processPayment):
        mock_processPayment.return_value = None
        response = self.app.post('/process-payment', data=json.dumps({'payment_data': 'test'}), content_type='application/json')
        assert response.status_code == 200

    @patch('src.main.integrateAPI')
    def test_api_integration(self, mock_integrateAPI):
        mock_integrateAPI.return_value = None
        response = self.app.post('/integrate-api', data=json.dumps({'api_data': 'test'}), content_type='application/json')
        assert response.status_code == 200

    @patch('src.main.networkClonedUser')
    def test_network_cloned_user(self, mock_networkClonedUser):
        mock_networkClonedUser.return_value = None
        response = self.app.post('/network-cloned-user', data=json.dumps({'user_data': 'test'}), content_type='application/json')
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()
```