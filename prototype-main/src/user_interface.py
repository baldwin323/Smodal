```python
from flask import Flask, render_template, request
import requests
from src.clone_training import startCloneTraining
from src.social_media_integration import connectToSocialMedia
from src.payment_processing import processPayment

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_clone_training', methods=['POST'])
def clone_training():
    user_data = request.get_json()
    startCloneTraining(user_data)
    return {'message': 'CloneTrainingStarted'}

@app.route('/connect_social_media', methods=['POST'])
def social_media_connect():
    user_data = request.get_json()
    connectToSocialMedia(user_data)
    return {'message': 'SocialMediaConnected'}

@app.route('/process_payment', methods=['POST'])
def payment_processing():
    payment_data = request.get_json()
    processPayment(payment_data)
    return {'message': 'PaymentProcessed'}

if __name__ == '__main__':
    app.run(debug=True)
```