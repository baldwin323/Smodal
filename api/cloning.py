from flask import Flask, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = '/path/to/upload'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file is sent
    if 'doc' not in request.files:
        return 'No file part'
    file = request.files['doc']
    
    # If user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        return 'No selected file'
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File successfully uploaded'

if __name__ == "__main__":
    app.run(debug=True)