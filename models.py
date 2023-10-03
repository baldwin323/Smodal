from django.db import models

class OpenAIIntegration(models.Model):
    api_key = models.CharField(max_length=255, blank=False, null=False, unique=True)

class OIDCConfiguration(models.Model):
    client_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    client_secret = models.CharField(max_length=255, blank=False, null=False, unique=True)
    redirect_uris = models.TextField(blank=False, null=False)