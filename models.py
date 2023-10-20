# Importing necessary libraries from Django
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.hashers import make_password

# Model for storing the credentials
class Credentials(models.Model):
    # Name of the platform
    platform = models.CharField(max_length=255, blank=False, null=False, unique=True)
    # Username of the account on the platform
    username = models.CharField(max_length=255, blank=False, null=False, unique=False)
    # Password of the account on the platform
    password = models.CharField(max_length=255, blank=False, null=False, unique=False)
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

# Model for storing the API credentials
class APICredentials(models.Model):
    # Name of the platform
    platform = models.CharField(max_length=255, blank=False, null=False, unique=True)
    # API key of the account on the platform
    api_key = models.CharField(max_length=255, blank=False, null=False, unique=True)
    # API secret of the account on the platform
    api_secret = models.CharField(max_length=255, blank=False, null=False, unique=True)
    
    def save(self, *args, **kwargs):
        self.api_secret = make_password(self.api_secret)
        super().save(*args, **kwargs)

# Model for storing OpenAI API integration details
class OpenAIIntegration(models.Model):
    # API key of the OpenAI account
    api_key = models.CharField(max_length=255, blank=False, null=False, unique=True)
    
    def save(self, *args, **kwargs):
        self.api_key = make_password(self.api_key)
        super().save(*args, **kwargs)

# Model for storing OIDC configuration
class OIDCConfiguration(models.Model):
    # Client ID of the OIDC account
    client_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    # Client secret of the OIDC account
    client_secret = models.CharField(max_length=255, blank=False, null=False, unique=True)
    # Redirection URIs for the OIDC account
    redirect_uris = models.TextField(blank=False, null=False)
    # JWT Token for the OIDC account
    jwt_token = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.client_secret = make_password(self.client_secret)
        super().save(*args, **kwargs)

# Model for storing encrypted sensitive data
class EncryptedSensitiveData(models.Model):
    # Name of the platform
    platform = models.CharField(max_length=255, blank=False, null=False, unique=True)
    # Encrypted data related to the platform
    encrypted_data = models.TextField(blank=False, null=False)