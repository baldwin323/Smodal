import logging
from flask import Flask, render_template, request, jsonify
from src.database import DB_CONNECTION

app = Flask('modal.tokai')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def hello_world():
  try:
    logger.info('Processing user request')
    headers = request.headers

    return render_template(
        'index.html',
        user_id=headers.get('X-Replit-User-Id', None),
        user_name=headers.get('X-Replit-User-Name', None),
        user_roles=headers.get('X-Replit-User-Roles', None),
        user_bio=headers.get('X-Replit-User-Bio', None),
        user_profile_image=headers.get('X-Replit-User-Profile-Image', None),
        user_teams=headers.get('X-Replit-User-Teams', None),
        user_url=headers.get('X-Replit-User-Url', None)
    )
  except Exception as e:
    logger.error('An error occurred while processing user request: %s', str(e))
    return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/clone', methods=['POST'])
def get_clone():
  try:
    logger.info('Generating clone content')
    data = request.get_json()
    prompt = data.get('prompt', None)
    tokens = data.get('tokens', None)

    if prompt is None or tokens is None:
      return jsonify({'error': 'Missing parameters in request'}), 400

    text = DB_CONNECTION.generate_content(prompt, tokens)
    return jsonify({'text': text})
  except Exception as e:
    logger.error('An error occurred while generating clone content: %s', str(e))
    return jsonify({'error': 'An error occurred while processing your request'}), 500

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)