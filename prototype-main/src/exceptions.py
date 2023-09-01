```python
class Error(Exception):
    """Base class for other exceptions"""
    pass

class CloneTrainingError(Error):
    """Raised when there is an issue with clone training"""
    pass

class SocialMediaConnectionError(Error):
    """Raised when there is an issue with social media connection"""
    pass

class PaymentProcessingError(Error):
    """Raised when there is an issue with payment processing"""
    pass

class APIIntegrationError(Error):
    """Raised when there is an issue with API integration"""
    pass

class NetworkingError(Error):
    """Raised when there is an issue with networking"""
    pass

class DatabaseConnectionError(Error):
    """Raised when there is an issue with the database connection"""
    pass
```