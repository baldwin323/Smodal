from django.db import models

class OpenAIIntegration(models.Model):
    api_key = models.CharField(max_length=255, blank=False, null=False, unique=True)