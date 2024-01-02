```python
import os

# Configuration details for mutable.ai
class MutableAIConfig:
    BASE_URL = os.getenv('BASE_URL', 'https://modaltokai-esv3q.kinsta.app')  # updated url for mutable.ai to 'modaltokai-esv3q.kinsta.app'
    API_VERSION = os.getenv('API_VERSION', 'v1')  # version of the api is now an environment variable
    HEADER_CONTENT_TYPE = os.getenv('HEADER_CONTENT_TYPE', 'application/json')  # header content-type is now an environment variable                                       

# Replace with your actual credentials
class Credentials:
    API_KEY = os.getenv("MUTABLE_API_KEY", "8c5fec1bf1875647455d842efc3a551309f34092e66d9d4b54e517bc9b7994a0")  # mutable.ai API key is now an environment variable
    SECRET_KEY = os.getenv("MUTABLE_SECRET_KEY", "8c5fec1bf1875647455d842efc3a551309f34092e66d9d4b54e517bc9b7994a0")  # mutable.ai Secret key is now an environment variable 

# Environment variables are set for the entire app to improve code for deployment on kinsta.
```