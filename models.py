from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
import secrets
from django.db.utils import IntegrityError
import os

os.getenv('DB_HOST', 'localhost')
os.getenv('DB_PORT', '5432')

class UserProfile(models.Model):
    birth_date = models.DateField(blank=True, null=True, db_index=True)  
    image = models.ImageField(upload_to='profile_images/', blank=True)
    preferences = models.JSONField(blank=True, null=True)
    theme_preferences = models.CharField(max_length=200, default="default")


class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'jpg', 'jpeg', 'png'])])
    token = models.CharField(max_length=255, default=secrets.token_urlsafe)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            # This exception mainly occurs due to unique constraint violation.
            print(f"Integrity Error: {e}")
        except Exception as e:
            # Catching all other exceptions
            print(f"An error occurred: {e}")


class Banking(models.Model):
    transactions = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            # Catching all exceptions during save operation on banking model
            print(f"An error occurred while saving banking transaction: {e}")


class AIConversation(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    previous_responses = models.JSONField(default=list)
    current_context = models.TextField()
    
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            # Catching all exceptions during save operation on AIConversation model
            print(f"An error occurred while saving AI conversation: {e}")


class UIPageData(models.Model):
    page_id = models.CharField(max_length=200)
    page_data = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            # Catching all exceptions during save operation on UIPageData model
            print(f"An error occurred while saving UI page data: {e}")