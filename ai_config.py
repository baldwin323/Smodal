```python
import os

# Configuration details for mutable.ai
class MutableAIConfig:
    BASE_URL = os.getenv('BASE_URL', 'https://api.mutable.ai')  # url for mutable.ai is now an environment variable.
    API_VERSION = os.getenv('API_VERSION', 'v1')  # version of the api is now an environment variable
    HEADER_CONTENT_TYPE = os.getenv('HEADER_CONTENT_TYPE', 'application/json')  # header content-type is now an environment variable                                       

# Replace with your actual credentials
class Credentials:
    API_KEY = os.getenv("MUTABLE_API_KEY", "<fill in api key>")  # mutable.ai API key is now an environment variable
    SECRET_KEY = os.getenv("MUTABLE_SECRET_KEY", "<fill in secret key>")  # mutable.ai Secret key is now an environment variable

# Included environment variables for the entire app to improve code for deployment on kinsta.
```
The placeholders "<fill in api key>" and "<fill in secret key>" in the .env file should be replaced with the actual keys for mutable.ai API.