from django.db import models
from django.core.validators import FileExtensionValidator
# Existing imports...

class UserProfile(models.Model):
    #...
    birth_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True)


class FileUpload(models.Model):
    #...
    file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'jpg', 'jpeg', 'png'])])


class Banking(models.Model):
    #...
    transactions = models.JSONField(default=dict)  


# Existing model classes...

# New model to maintain state between interactions
class AIConversation(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Link to the user (or session)
    previous_responses = models.JSONField(default=list)  # Store previous responses here
    current_context = models.TextField()  # Current conversation context, as understood by the AI

# This model will help the AI to maintain a memory of its engagement with each user,
# across different social media sites and the website. The 'context' field should be updated
# every time the AI sends or receives a message.