```python
from pymongo import MongoClient
from src.config import APP_CONFIG

class Database:
    def __init__(self):
        self.client = MongoClient(APP_CONFIG['DATABASE_URL'])
        self.db = self.client['modal_tok_ai']

    def get_user(self, user_id):
        return self.db.users.find_one({'_id': user_id})

    def save_user(self, user_data):
        return self.db.users.insert_one(user_data)

    def get_clone(self, clone_id):
        return self.db.clones.find_one({'_id': clone_id})

    def save_clone(self, clone_data):
        return self.db.clones.insert_one(clone_data)

    def get_payment(self, payment_id):
        return self.db.payments.find_one({'_id': payment_id})

    def save_payment(self, payment_data):
        return self.db.payments.insert_one(payment_data)

DB_CONNECTION = Database()
```