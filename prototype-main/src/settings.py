
```
from flask import Flask, request, jsonify

app = Flask(__name__)

user_settings = {
    'username': '',
    'password': '',
    'email': '',
    'notifications': True,
}

@app.route('/settings', methods=['GET', 'POST'])
def handle_settings():
    if request.method == 'POST':
        new_settings = request.json
        for key, value in new_settings.items():
            if key in user_settings:
                user_settings[key] = value
        return jsonify(user_settings), 200
    else:
        return jsonify(user_settings), 200

if __name__ == "__main__":
    app.run(debug=True)
```