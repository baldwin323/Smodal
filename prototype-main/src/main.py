```python
from flask import Flask, request
from src.user_interface import UserInterface
from src.clone_training import startCloneTraining
from src.social_media_integration import connectToSocialMedia
from src.payment_processing import processPayment
from src.api_integration import integrateAPI
from src.networking import networkClonedUser
from src.database import DB_CONNECTION
from src.config import APP_CONFIG

app = Flask(__name__)

@app.route('/')
def home():
    return UserInterface().render()

@app.route('/start-clone-training', methods=['POST'])
def clone_training():
    user_data = request.get_json()
    startCloneTraining(user_data)
    return {'message': 'CloneTrainingStarted'}

@app.route('/connect-social-media', methods=['POST'])
def social_media_connect():
    user_data = request.get_json()
    connectToSocialMedia(user_data)
    return {'message': 'SocialMediaConnected'}

@app.route('/process-payment', methods=['POST'])
def payment_processing():
    payment_data = request.get_json()
    processPayment(payment_data)
    return {'message': 'PaymentProcessed'}

@app.route('/integrate-api', methods=['POST'])
def api_integration():
    api_data = request.get_json()
    integrateAPI(api_data)
    return {'message': 'APIIntegrated'}

@app.route('/network-cloned-user', methods=['POST'])
def network_cloned_user():
    user_data = request.get_json()
    networkClonedUser(user_data)
    return {'message': 'ClonedUserNetworked'}

if __name__ == '__main__':
    app.run(host=APP_CONFIG['HOST'], port=APP_CONFIG['PORT'])
```