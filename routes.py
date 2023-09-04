from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import requests
from pymongo import MongoClient

app = Flask(__name__)

API_NAME = '' # API name can be accessed from environment variables
UPLOAD_FOLDER = '/path/to/upload' # the path can be updated to your desired file location
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient(' mongodb+srv://[username:password@clusterurl/test?retryWrites=true&w=majority') # Replace MongoDB connection string here
db = client['some-database'] # Replace with your database name
collection = db['some-collection'] # Replace with your collection name

# Route to handle API communication 
@app.route('/api', methods=['POST'])
def api_request():
    api_name = request.form['apiName']
    if api_name == API_NAME:
        # Add logic for authenticating with the API and making requests here
        response = requests.get('https://some-api.com/{api_name}'.format(api_name=api_name))
        return response.json()
    else:
        return 'Invalid API name!', status.HTTP_400_BAD_REQUEST

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', status.HTTP_400_BAD_REQUEST
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', status.HTTP_400_BAD_REQUEST

    if file:
        filename = secure_filename(file.filename)
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(uploaded_file_path)
        
        doc = {
            'filename': filename,
            'filepath': uploaded_file_path,
            'uploaded_by': request.user
        }
        collection.insert_one(doc) # Save document details in MongoDB

        return 'File successfully uploaded', status.HTTP_200_OK

    return 'Something went wrong with file upload!', status.HTTP_500_INTERNAL_SERVER_ERROR

# Route to get file by id
@app.route('/files/<id>', methods=['GET'])
def get_file(id):
    file_metadata = collection.find_one({'_id': id})

    if file_metadata:
        return send_from_directory(file_metadata['filepath'], file_metadata['filename'])
    else:
        return 'File not found!', status.HTTP_404_NOT_FOUND

if __name__ == "__main__":
    app.run()