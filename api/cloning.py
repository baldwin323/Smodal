from flask import Flask, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "/path/to/upload"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_file():
    # Check if a file is sent
    if "doc" not in request.files:
        return "No file part", 400

    file = request.files["doc"]

    # If user does not select file, browser also submit an empty part without filename
    if file.filename == "":
        return "No selected file", 400

    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return "File successfully uploaded", 200
        except:
            return "An error occurred while saving the file", 500
    else:
        return "File type not allowed", 400


if __name__ == "__main__":
    app.run(debug=True)
