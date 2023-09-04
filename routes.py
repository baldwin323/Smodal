from flask import Flask, request, send_from_directory, abort
from werkzeug.utils import secure_filename
import os
import requests
from pymongo import MongoClient
from http import HTTPStatus

app = Flask(__name__)

API_NAME = os.getenv('API_NAME') # API name can be accessed from environment variables
UPLOAD_FOLDER = '/path/to/upload' # the path can be updated to your desired file location
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient('mongodb+srv://[username:password@clusterurl/test?retryWrites=true&w=majority') # Replace MongoDB connection string here
db = client['some-database'] # Replace with your database name
collection = db['some-collection'] # Replace with your collection name

# Route to handle API communication 
@app.route('/api', methods=['POST'])
def api_request():
    if 'apiName' not in request.form:
        abort(HTTPStatus.BAD_REQUEST, 'No API name provided')
    api_name = request.form['apiName']
    if api_name == API_NAME:
        # Add logic for authenticating with the API and making requests here
        response = requests.get(f'https://some-api.com/{api_name}')
        if response.status_code != HTTPStatus.OK:
            abort(response.status_code)
        return response.json()
    else:
        abort(HTTPStatus.BAD_REQUEST, 'Invalid API name')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(HTTPStatus.BAD_REQUEST, 'No file part')
    file = request.files['file']
    if file.filename == '':
        abort(HTTPStatus.BAD_REQUEST, 'No selected file')
    if file:
        filename = secure_filename(file.filename)
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(uploaded_file_path)
        doc = {
            'filename': filename,
            'filepath': uploaded_file_path,
            'uploaded_by': request.remote_addr
        }
        collection.insert_one(doc) # Save document details in MongoDB
        return {'message': 'File successfully uploaded'}, HTTPStatus.OK
    abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Something went wrong with file upload!')

# Route to get file by id
@app.route('/files/<id>', methods=['GET'])
def get_file(id):
    file_metadata = collection.find_one({'_id': id})

    if file_metadata:
        return send_from_directory(file_metadata['filepath'], file_metadata['filename'])
    else:
        abort(HTTPStatus.NOT_FOUND, 'File not found')

if __name__ == "__main__":
    app.run()