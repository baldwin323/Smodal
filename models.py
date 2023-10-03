from django.db import models

class Credentials(models.Model):
    platform = models.CharField(max_length=255, blank=False, null=False, unique=True)
    username = models.CharField(max_length=255, blank=False, null=False, unique=False)
    password = models.CharField(max_length=255, blank=False, null=False, unique=False)
    
class APICredentials(models.Model):
    platform = models.CharField(max_length=255, blank=False, null=False, unique=True)
    api_key = models.CharField(max_length=255, blank=False, null=False, unique=True)
    api_secret = models.CharField(max_length=255, blank=False, null=False, unique=True)

class OpenAIIntegration(models.Model):
    api_key = models.CharField(max_length=255, blank=False, null=False, unique=True)

class OIDCConfiguration(models.Model):
    client_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    client_secret = models.CharField(max_length=255, blank=False, null=False, unique=True)
    redirect_uris = models.TextField(blank=False, null=False)
    
class EncryptedSensitiveData(models.Model):
    platform = models.CharField(max_length=255, blank=False, null=False, unique=True)
    encrypted_data = models.TextField(blank=False, null=False, unique=False)