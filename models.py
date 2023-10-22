# Importing necessary libraries from Django
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.hashers import make_password

# Validates that necessary fields are provided
def validate_fields(value):
    if not value:
        raise ValidationError("This field is required. Please provide it.")
        
# Encrypts sensitive information before it's saved
def encrypt_data(data):
    return make_password(data)


# Model for storing the credentials
class Credentials(models.Model):
    # Name of the platform
    platform = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    # Username of the account on the platform
    username = models.CharField(max_length=255, blank=False, null=False, unique=False, validators=[validate_fields])
    # Password of the account on the platform
    password = models.CharField(max_length=255, blank=False, null=False, unique=False, validators=[validate_fields])
    
    def save(self, *args, **kwargs):
        self.password = encrypt_data(self.password)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Credentials"

# Model for storing the API credentials
class APICredentials(models.Model):
    # Name of the platform
    platform = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    # API key of the account on the platform
    api_key = models.CharField(max_length=255, blank=False, null=False, unique=False, validators=[validate_fields])
    # API secret of the account on the platform
    api_secret = models.CharField(max_length=255, blank=False, null=False, unique=False, validators=[validate_fields])
    
    def save(self, *args, **kwargs):
        self.api_secret = encrypt_data(self.api_secret)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "API Credentials"

# Model for storing OpenAI API integration details
class OpenAIIntegration(models.Model):
    # API key of the OpenAI account
    api_key = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    
    def save(self, *args, **kwargs):
        self.api_key = encrypt_data(self.api_key)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "OpenAI Integrations"

# Model for storing OIDC configuration
class OIDCConfiguration(models.Model):
    # Client ID of the OIDC account
    client_id = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    # Client secret of the OIDC account
    client_secret = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    # Redirection URIs for the OIDC account
    redirect_uris = models.TextField(blank=False, null=False, validators=[validate_fields])
    # JWT Token for the OIDC account
    jwt_token = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.client_secret = encrypt_data(self.client_secret)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "OIDC Configurations"

# Model for storing encrypted sensitive data
class EncryptedSensitiveData(models.Model):
    # Name of the platform
    platform = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    # Encrypted data related to the platform
    encrypted_data = models.TextField(blank=False, null=False, validators=[validate_fields])
    
    class Meta:
        verbose_name_plural = "Encrypted Sensitive Data"