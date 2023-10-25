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