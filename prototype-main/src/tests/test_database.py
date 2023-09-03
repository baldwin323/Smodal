```python
import unittest
from pymongo import MongoClient
from src.database import Database
from unittest.mock import patch

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Database()

    @patch('pymongo.collection.Collection.find_one')
    def test_get_user(self, mock_find):
        self.db.get_user('test_id')
        mock_find.assert_called_with({'_id': 'test_id'})

    @patch('pymongo.collection.Collection.insert_one')
    def test_save_user(self, mock_insert):
        user_data = {'_id': 'test_id', 'name': 'Test User'}
        self.db.save_user(user_data)
        mock_insert.assert_called_with(user_data)

    @patch('pymongo.collection.Collection.find_one')
    def test_get_clone(self, mock_find):
        self.db.get_clone('clone_id')
        mock_find.assert_called_with({'_id': 'clone_id'})

    @patch('pymongo.collection.Collection.insert_one')
    def test_save_clone(self, mock_insert):
        clone_data = {'_id': 'clone_id', 'name': 'Test Clone'}
        self.db.save_clone(clone_data)
        mock_insert.assert_called_with(clone_data)

    @patch('pymongo.collection.Collection.find_one')
    def test_get_payment(self, mock_find):
        self.db.get_payment('payment_id')
        mock_find.assert_called_with({'_id': 'payment_id'})

    @patch('pymongo.collection.Collection.insert_one')
    def test_save_payment(self, mock_insert):
        payment_data = {'_id': 'payment_id', 'amount': 100.0}
        self.db.save_payment(payment_data)
        mock_insert.assert_called_with(payment_data)


if __name__ == '__main__':
    unittest.main()
```