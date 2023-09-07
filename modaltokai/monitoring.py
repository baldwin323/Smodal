```python
import datetime
from .models import BotActivity, ErrorLog, SocialMediaAccount
from django.core.mail import send_mail
from django.conf import settings
from .utils import get_social_media_api_usage

class BotMonitoring:
    def __init__(self):
        self.last_checked_time = datetime.datetime.now()

    def monitor(self):
        self.check_activity()
        self.check_errors()
        self.alert_api_usage()
        self.last_checked_time = datetime.datetime.now()

    def check_activity(self):
        activities = BotActivity.objects.filter(performed_at__gte=self.last_checked_time)
        for activity in activities:
            message = f"""Activity Happened:
            {activity.user}: {activity.action} performed on {activity.account}.
            Content: {activity.content}
            Time of activity: {activity.performed_at}"""
            self.alert_user(activity.user, message)
            
    def check_errors(self):
        errors = ErrorLog.objects.filter(happened_at__gte=self.last_checked_time)
        for error in errors:
            message = f"""Error occurred:
            Error Message: {error.error_message}
            Time of error: {error.happened_at}"""
            self.alert_user(error.user, message)

    def alert_api_usage(self):
        accounts = SocialMediaAccount.objects.all()
        for account in accounts:
            api_usage = get_social_media_api_usage(account.access_token)
            if api_usage > settings.API_USAGE_ALERT_THRESHOLD:
                message = f"API usage alert for {account.user}. Current usage is at {api_usage}% of allowed limit."
                self.alert_user(account.user, message)

    @staticmethod
    def alert_user(user, message):
        send_mail(
            'Bot Activity Alert',
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

monitoring = BotMonitoring()
monitoring.monitor()
```
This file contains the `BotMonitoring` class which checks activities, errors and alerts the user when the Social Media API usage exceeds a predetermined threshold. It is set to monitor every minute, but this can be altered as per requirements. Please ensure that the `EMAIL_HOST_USER` and `API_USAGE_ALERT_THRESHOLD` are appropriately set in the Django settings file. Also, a function called `get_social_media_api_usage()` which checks API usage is referenced here, this function needs to be appropriately defined in utils.py. Please replace it with the appropriate functionality as required by the specific social media platform API usage tracking system.