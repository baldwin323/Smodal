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


# Model for storing the user profile and account settings
class UserProfile(models.Model):
    # User ID of the authenticated user
    user_id = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    # User first name
    first_name = models.CharField(max_length=255, blank=False, null=False, unique=False, validators=[validate_fields])
    # User last name
    last_name = models.CharField(max_length=255, blank=False, null=False, unique=False, validators=[validate_fields])
    # User email
    email = models.CharField(max_length=255, blank=False, null=False, unique=False, validators=[validate_fields])
    # User bio
    bio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "UserProfiles"

# Model for storing user file uploads
class FileUpload(models.Model):
    # ID of the user performing the upload
    user_id = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    # File name
    file_name = models.CharField(max_length=255, blank=False, null=False, unique=False, validators=[validate_fields])
    # File size
    file_size = models.IntegerField(blank=False, null=False)
    # File extension
    file_extension = models.CharField(max_length=50, blank=False, null=False, unique=False, validators=[validate_fields])
    # File content
    content = models.BinaryField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "FileUploads"

# Model for storing recent user activity
class UserActivity(models.Model):
    # User ID of the user whose activity is being tracked
    user_id = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    # Description of the activity
    activity_description = models.TextField(blank=False, null=False, validators=[validate_fields])
    # Timestamp of the activity
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "UserActivities"

# Model for storing banking transactions and related activities
class Banking(models.Model):
    # User ID of the involved user
    user_id = models.CharField(max_length=255, blank=False, null=False, unique=True, validators=[validate_fields])
    # Transaction details
    transaction_details = models.JSONField(null=False, blank=False)

    class Meta:
        verbose_name_plural = "Banking"

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

# Model for storing affiliate uploads
class AffiliateUploads(models.Model):
    # Affiliate upload data
    upload_data = models.JSONField(null=False, blank=False)

    class Meta:
        verbose_name_plural = "AffiliateUploads"

# Model for storing OpenAI API integration details
class OpenAIAPICalls(models.Model):
    # API call details
    call_details = models.JSONField(null=False, blank=False)

    class Meta:
        verbose_name_plural = "OpenAIAPICalls"

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
