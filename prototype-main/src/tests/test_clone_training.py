```python
import unittest
from src.clone_training import startCloneTraining
from unittest.mock import patch, MagicMock
from pymongo.errors import PyMongoError

class TestCloneTraining(unittest.TestCase):
    @patch("src.api_integration.integrateAPI", return_value= {"clone_data": "data"})
    @patch("src.clone_training.DB_CONNECTION")
    @patch("src.networking.networkClonedUser", return_value=True)
    def test_startCloneTraining_success(self, mock_networkClonedUser, mock_db, mock_api):
        # Mock DB calls
        mock_db.find_one.return_value = {"_id": "user_id", "api_key": "api_key"}
        mock_db.insert_one.return_value = MagicMock(inserted_id="clone_id")

        # Start training
        result = startCloneTraining("user_id")

        # Check results
        self.assertEqual(result, "clone_id")
        mock_db.find_one.assert_called_with({"_id": "user_id"})
        mock_api.assert_called_with("api_key")
        mock_db.insert_one.assert_called_with({"clone_data": "data"})
        mock_networkClonedUser.assert_called_with("clone_id")

    @patch("src.api_integration.integrateAPI", return_value= {"clone_data": "data"})
    @patch("src.clone_training.DB_CONNECTION")
    @patch("src.networking.networkClonedUser", return_value=True)
    def test_startCloneTraining_user_not_found(self, mock_networkClonedUser, mock_db, mock_api):
        # Mock DB calls
        mock_db.find_one.return_value = None

        # Expect User not found exception
        self.assertRaises(Exception, startCloneTraining, "wrong_id")

    @patch("src.api_integration.integrateAPI", return_value= None)
    @patch("src.clone_training.DB_CONNECTION")
    @patch("src.networking.networkClonedUser", return_value=True)
    def test_startCloneTraining_failed_api_integration(self, mock_networkClonedUser, mock_db, mock_api):
        # Mock DB calls
        mock_db.find_one.return_value = {"_id": "user_id", "api_key": "api_key"}

        # Expect Failed to fetch clone data exception
        self.assertRaises(Exception, startCloneTraining, "user_id")

    @patch("src.api_integration.integrateAPI", return_value= {"clone_data": "data"})
    @patch("src.clone_training.DB_CONNECTION")
    @patch("src.networking.networkClonedUser", return_value=False)
    def test_startCloneTraining_network_failure(self, mock_networkClonedUser, mock_db, mock_api):
        # Mock DB calls
        mock_db.find_one.return_value = {"_id": "user_id", "api_key": "api_key"}
        mock_db.insert_one.return_value = MagicMock(inserted_id="clone_id")

        # Expect Failed to network clone exception
        self.assertRaises(Exception, startCloneTraining, "user_id")

    @patch("src.api_integration.integrateAPI", return_value= {"clone_data": "data"})
    @patch("src.clone_training.DB_CONNECTION")
    @patch("src.networking.networkClonedUser", return_value=True)
    def test_startCloneTraining_db_insert_failure(self, mock_networkClonedUser, mock_db, mock_api):
        # Mock DB calls
        mock_db.find_one.return_value = {"_id": "user_id", "api_key": "api_key"}
        mock_db.insert_one.side_effect = PyMongoError('DB error')

        # Expect Failed to save clone data exception
        self.assertRaises(Exception, startCloneTraining, "user_id")

if __name__ == '__main__':
    unittest.main()
```