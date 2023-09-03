```python
import requests
import unittest
from unittest.mock import patch
from src.exceptions import NetworkError
from src.networking import networkClonedUser

class TestNetworkClonedUser(unittest.TestCase):

    @patch('src.networking.requests.post')
    def test_networkClonedUser_success(self, mock_post):
        mock_post.return_value.status_code = 200
        self.assertTrue(networkClonedUser("test_user_id", 'test_clone_id'))

    @patch('src.networking.requests.post')
    def test_networkClonedUser_network_error(self, mock_post):
        mock_post.return_value.status_code = 400
        self.assertRaises(NetworkError, networkClonedUser, "test_user_id", 'test_clone_id')

    @patch('src.networking.requests.post')
    def test_networkClonedUser_exception(self, mock_post):
        mock_post.side_effect = Exception()
        self.assertRaises(NetworkError, networkClonedUser, "test_user_id", "test_clone_id")
        

if __name__ == '__main__':
    unittest.main()
```
