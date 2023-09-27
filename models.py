from django.db import models

class OpenAIIntegration(models.Model):
    api_key = models.CharField(max_length=255, blank=False, null=False, unique=True)
# Improvements made: API key field is not nullable, cannot be blank, and must be unique. This enforces the necessary constraints on this field.