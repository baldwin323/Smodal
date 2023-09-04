
```python
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import requests
from src.clone_training import startCloneTraining
from src.social_media_integration import connectToSocialMedia
from src.payment_processing import processPayment

# Define text input form
class TextInputForm(FlaskForm):
    text_input = StringField('Text Input')
    submit = SubmitField('Submit')

# Define chat bubble form
class ChatBubbleForm(FlaskForm):
    message = StringField('Message')
    submit = SubmitField('Submit')

# Define widget form
class WidgetForm(FlaskForm):
    content = StringField('Widget Content')
    submit = SubmitField('Submit')

# Define button form
class ButtonForm(FlaskForm):
    clicked = SubmitField('Click Button')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Your-Secret-Key'  # Use styled components or CSS modules for styling

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_clone_training', methods=['POST'])
def clone_training():
    form = TextInputForm()  # Use form in route
    if form.validate_on_submit():
        startCloneTraining(form.text_input.data)
        return {'message': 'CloneTrainingStarted'}
    return render_template('clone_training.html', form=form)

@app.route('/connect_social_media', methods=['POST'])
def social_media_connect():
    form = TextInputForm()  # Use form in route
    if form.validate_on_submit():
        connectToSocialMedia(form.text_input.data)
        return {'message': 'SocialMediaConnected'}
    return render_template('social_media_connect.html', form=form)

@app.route('/process_payment', methods=['POST'])
def payment_processing():
    form = TextInputForm()  # Use form in route
    if form.validate_on_submit():
        processPayment(form.text_input.data)
        return {'message': 'PaymentProcessed'}
    return render_template('payment_processing.html', form=form)

@app.route('/voice_input', methods=['POST'])
def voice_input():
    form = TextInputForm()  # Use form in route
    # Add functionality to process and utilize voice data
    if form.validate_on_submit():
        # Process voice data
        return {'message': 'VoiceInputReceived'}
    return render_template('voice_input.html', form=form)

@app.route('/text_input', methods=['POST'])
def text_input():
    form = TextInputForm()  # Use form in route
    # Add functionality to process and utilize text data
    if form.validate_on_submit():
        # Process text data
        return {'message': 'TextInputReceived'}
    return render_template('text_input.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
```