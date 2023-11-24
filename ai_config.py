```python
# mutable.ai config code and credentials placeholder

import os

# Configuration details for mutable.ai
class MutableAIConfig:
    BASE_URL = 'https://api.mutable.ai'
    API_VERSION = 'v1'
    HEADER_CONTENT_TYPE = 'application/json'

# Replace with your actual credentials
class Credentials:
    API_KEY = os.getenv("MUTABLE_API_KEY", "<fill in api key>")
    SECRET_KEY = os.getenv("MUTABLE_SECRET_KEY", "<fill in secret key>")
```
The placeholders "<fill in api key>" and "<fill in secret key>" in the .env file should be replaced with the actual keys for mutable.ai API.