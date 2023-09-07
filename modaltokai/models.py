```python
from django.db import models
from django.contrib.auth.models import User

class SocialMediaApp(models.Model):
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)

class SocialMediaAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(SocialMediaApp, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200, null=True, blank=True)
    token_authorized_at = models.DateTimeField(auto_now_add=True)

class BotConfiguration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule_time = models.TimeField()
    engage_actions = models.TextField()
    monitor_keywords = models.TextField()

class BotActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    content = models.TextField()
    performed_at = models.DateTimeField(auto_now_add=True)

class ErrorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE, null=True, blank=True)
    error_message = models.TextField()
    happened_at = models.DateTimeField(auto_now_add=True)
```
Here, we have created models for 
- SocialMediaApp: represents the social media platforms for which you need access tokens.
- SocialMediaAccount: represent the authenticated social media accounts for each user.
- BotConfiguration: represents bot configurations that the user sets.
- BotActivity: keeps a record of each bot activity.
- ErrorLog: logs all errors happened during bot activity. This will include any exceptions caught during bot activity.
These models should ensure a smooth user experience and maintain all relevant data. The data you are storing should be enough to carry out all bot activities. Please make sure that all secret data are stored securely.