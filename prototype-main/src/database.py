```python
from pymongo import MongoClient
from openai import OpenAI
from src.config import APP_CONFIG

class Database:
    def __init__(self):
        self.client = MongoClient(APP_CONFIG['DATABASE_URL'])
        self.db = self.client['modal_tok_ai']
        self.openai = OpenAI(APP_CONFIG['OPENAI_API_KEY'])
        self.builderio = BuilderIO(APP_CONFIG['BUILDERIO_API_KEY'])

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
        
    # New methods added for Conversations and Responses
    def get_conversation(self, conversation_id):
        return self.db.conversations.find_one({'_id': conversation_id})

    def save_conversation(self, conversation_data):
        return self.db.conversations.insert_one(conversation_data)
        
    def get_response(self, response_id):
        return self.db.responses.find_one({'_id': response_id})

    def save_response(self, response_data):
        return self.db.responses.insert_one(response_data)

    # Methods for OpenAI and Builder.io interactions
    def generate_content(self, prompt, tokens):
        response = self.openai.Complete.create(
            engine="davinci-codex",
            prompt=prompt,
            max_tokens=tokens,
        )
        return response.choices[0].text.strip()

    def get_builderio_template(self, template_id):
        template = self.builderio.get(template_id)
        return template

DB_CONNECTION = Database()
```
