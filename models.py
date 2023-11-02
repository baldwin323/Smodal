from django.db import models
from django.core.validators import FileExtensionValidator
# Existing imports...

class UserProfile(models.Model):
    # Here identity fields of a user like birth_date, image, etc. are maintained.
    #...
    birth_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True)


class FileUpload(models.Model):
    # This model is used for file handling. It only allows extensions provided in the list.
    #...
    file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'jpg', 'jpeg', 'png'])])

    def save(self, *args, **kwargs):
        # Add error handling here
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")


class Banking(models.Model):
    # This model handles banking transactions in JSON format.
    #...
    transactions = models.JSONField(default=dict)  

    # Error handling for this class
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred while saving banking transaction: {e}")


# Existing model classes...

# New model class to maintain state between interactions with the AI model
class AIConversation(models.Model):
    # Link to the user (or session) is maintained by the ForeignKey relationship with UserProfile.
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  
    # History of previous responses that were sent by the AI.
    previous_responses = models.JSONField(default=list)  
    # Current conversation context, as understood by the AI is maintained in a TextField,
    # this will be updated every time the AI sends or receives a message.
    current_context = models.TextField()  

    def save(self, *args, **kwargs):
        # Error handling for AIConversation.
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred while saving AI conversation: {e}")

# Model class to handle UI page data
class UIPageData(models.Model):
    # Mapping with the available page ids in the frontend code
    page_id = models.CharField(max_length=200)
    # Data to be returned when API is called for this page
    page_data = models.JSONField(default=dict)
    
    def save(self, *args, **kwargs):
        # Error handling for UIPageData.
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred while saving UI page data: {e}")

# Model structure has been redesigned to meet the needs of state management, interaction history, user data,
# file management and banking transactions. The UIPageData model was further added to handle data for UI pages.