# This is the Procfile for Kinsta deployment

# Update: Modifying to use a "Process Control System" to manage both Node app and Python app in the same Pod. 
# Now using Supervisor to manage the processes

# web: Defines the command to start the web server. This has been updated for Kinsta deployment.
# It sources /etc/profile.d/kinsta_prompt.sh first to ensure proper environment setup
# Modified to ensure kinsta_prompt.sh is sourced by bash or a shell compatible with [[ syntax]]
# Updated to run 'app.js' with node
web: bash -c "source /etc/profile.d/kinsta_prompt.sh && supervisor -n exit /smodal/app.js"

# worker: Defines the command to start the worker process, configured for Kinsta deployment.
# Replaces previously EB specific configuration with generic configuration viable for any NGINX server
# Updated for Python app management using supervisor, assumed Python app is a worker.
# For this project, the command is supervisor -n exit python /path/to/pythonapp -c /etc/nginx/nginx.conf -g 'daemon off;'
worker: bash -c "source /etc/profile.d/kinsta_prompt.sh && supervisor -n exit python /path/to/pythonapp -c /etc/nginx/nginx.conf -g 'daemon off;'"

# Please note, this may need to be adjusted depending on the specific worker process configuration needed for the nginx server.