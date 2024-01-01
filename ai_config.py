```python
import os

# Configuration details for modal.tokai
class ModalTokaiConfig:
    BASE_URL = os.getenv('BASE_URL', 'https://api.modal.tokai')  # Updated URL for modal.tokai
    API_VERSION = os.getenv('API_VERSION', 'v1')  # version of the api is now an environment variable
    HEADER_CONTENT_TYPE = os.getenv('HEADER_CONTENT_TYPE', 'application/json')  # header content-type is now an environment variable                                      
                                                                
# Replace with your actual credentials
class Credentials:
    # Updated API key and secret key environment variables, which are specific to modal.tokai now
    API_KEY = os.getenv("MODAL_TOKAI_API_KEY", "8c5fec1bf1875647455d842efc3a551309f34092e66d9d4b54e517bc9b7994a0") 
    SECRET_KEY = os.getenv("MODAL_TOKAI_SECRET_KEY", "8c5fec1bf1875647455d842efc3a551309f34092e66d9d4b54e517bc9b7994a0") 

# Completed environment variables for the entire app to improve code for deployment on Kinsta.
```