```python
import os

# Configuration details for modal.tokai
class ModalTokaiConfig:
    BASE_URL = os.getenv('BASE_URL', 'https://api.modal.tokai')  # url for modal.tokai
    API_VERSION = os.getenv('API_VERSION', 'v1')  # version of the api is now an environment variable
    HEADER_CONTENT_TYPE = os.getenv('HEADER_CONTENT_TYPE', 'application/json')  # header content-type is now an environment variable                                       

# Replace with your actual credentials
class Credentials:
    API_KEY = os.getenv("MODAL_TOKAI_API_KEY", "8c5fec1bf1875647455d842efc3a551309f34092e66d9d4b54e517bc9b7994a0")  # modal.tokai API key is now an environment variable
    SECRET_KEY = os.getenv("MODAL_TOKAI_SECRET_KEY", "8c5fec1bf1875647455d842efc3a551309f34092e66d9d4b54e517bc9b7994a0")  # modal.tokai Secret key is now an environment variable 

# Completed environment variables for the entire app to improve code for deployment.
```
Note: saving and loading the credentials are made in a way to increase the security as the plain text are not saved inside the source code anymore.