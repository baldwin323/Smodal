# This is the Procfile for Kinsta deployment.

# web: Defines the command to start the web server. This has been updated for Kinsta deployment.
# Modified to use "web: gunicorn helloworld.wsgi" to run the web server as per Kinsta's instructions. 
# It sources /etc/profile.d/kinsta_prompt.sh first to ensure proper environment setup.
# This has been modified appropriately to fit the new command and ensure proper functioning with Kinsta.
web: bash -c "source /etc/profile.d/kinsta_prompt.sh && gunicorn helloworld.wsgi"

# worker: Defines the command to start the worker process, configured for Kinsta deployment.
# Replaces previously EB specific configuration with generic configuration viable for any NGINX server.
# For this project, the command is nginx -c /etc/nginx/nginx.conf -g 'daemon off;'
worker: nginx -c /etc/nginx/nginx.conf -g 'daemon off;'
# Please note, this may need to be adjusted depending on the specific worker process configuration needed for the nginx server.