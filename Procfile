
# This is the Procfile for Kinsta deployment

# web: Defines the command to start the web server. Currently setting up gunicorn to run the app.
# It sources /etc/profile.d/kinsta_prompt.sh first to set up necessary environment.
# Modified to ensure kinsta_prompt.sh is sourced by bash or a shell compatible with [[ syntax]]
web: bash -c "source /etc/profile.d/kinsta_prompt.sh && gunicorn app:app"

# worker: Defines the command to start the worker process
worker: python worker.py