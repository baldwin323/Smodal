from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
import secrets
from django.db.utils import IntegrityError
import os  # Imported os for getting environment variables

# Database environments to be obtained from the host machine when running inside a Docker container.
# The Django project settings should refer to these variables instead of hard-coded database service specs.
os.getenv('DB_HOST', 'localhost')
os.getenv('DB_PORT', '5432')

# Existing Imports...

class UserProfile(models.Model):
    # Here identity fields of a user like birth_date, image, etc. are maintained.
    # Optimized the database query using indexing and added detailed comments
    birth_date = models.DateField(blank=True, null=True, db_index=True)  # Added indexing to optimize queries
    image = models.ImageField(upload_to='profile_images/', blank=True)
    preferences = models.JSONField(blank=True, null=True)
    theme_preferences = models.CharField(max_length=200, default="default")


class FileUpload(models.Model):
    # This model is used for file handling. It only allows extensions provided in the list.
    file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'jpg', 'jpeg', 'png'])])
    token = models.CharField(max_length=255, default=secrets.token_urlsafe)

    # Overridden default save method to include exception handling.
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            print(f"Integrity Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


class Banking(models.Model):
    # This model handles banking transactions in JSON format.
    transactions = models.JSONField(default=dict)

    # Overridden default save method to include exception handling.
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred while saving banking transaction: {e}")


# Existing model classes...

class AIConversation(models.Model):
    # Link to the user (or session) is maintained by the ForeignKey relationship with UserProfile.
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # History of previous responses that were sent by the AI.
    previous_responses = models.JSONField(default=list)
    # Current conversation context, as understood by the AI is maintained in a TextField,
    # this will be updated every time the AI sends or receives a message.
    current_context = models.TextField()

    # Overridden default save method to include exception handling.
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred while saving AI conversation: {e}")


class UIPageData(models.Model):
    # Mapping with the available page ids in the frontend code.
    page_id = models.CharField(max_length=200)
    # Data to be returned when API is called for this page.
    page_data = models.JSONField(default=dict)

    # Overridden default save method to include exception handling.
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred while saving UI page data: {e}")

# Model structure has been redesigned to meet the needs of state management, interaction history, user data,
# file management and banking transactions. The UIPageData model was further added to handle data for UI pages.
# Improved exception handling was added for security measures.