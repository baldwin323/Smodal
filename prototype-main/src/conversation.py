```python
class Conversation:
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.history = []
        
    def start_conversation(self):
        self.history = []
        
    def generate_response(self, input):
        # TODO: Use model to generate response using input
        response = "Model response goes here"
        return response
    
    def save_conversation(self):
        # TODO: Save conversation history to database
        pass
```