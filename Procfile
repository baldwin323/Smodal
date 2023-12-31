
# This is the Procfile for Kinsta deployment

# web: Defines the command to start the web server. This has been updated from using gunicorn to nginx.
# It sources /etc/profile.d/kinsta_prompt.sh first to set up necessary environment.
# Modified to ensure kinsta_prompt.sh is sourced by bash or a shell compatible with [[ syntax]]
web: bash -c "source /etc/profile.d/kinsta_prompt.sh && nginx -g 'daemon off;'"

# worker: Defines the command to start the worker process, this has to be updated based on the nginx worker process.
worker: <nginx worker command>
# Replace the placeholder <nginx worker command> with the appropriate command to start the nginx worker process.