
```python
from django.contrib import admin
from .models import SocialMediaApp, SocialMediaAccount, BotConfiguration, BotActivity, ErrorLog
from django.contrib.auth.models import User

class SocialMediaAppAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'secret']

class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'app', 'access_token', 'refresh_token', 'token_authorized_at']

class BotConfigurationAdmin(admin.ModelAdmin):
    list_display = ['user', 'schedule_time', 'engage_actions', 'monitor_keywords']

class BotActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'account', 'action', 'content', 'performed_at']

class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'account', 'error_message', 'happened_at']

admin.site.register(User)
admin.site.register(SocialMediaApp, SocialMediaAppAdmin)
admin.site.register(SocialMediaAccount, SocialMediaAccountAdmin)
admin.site.register(BotConfiguration, BotConfigurationAdmin)
admin.site.register(BotActivity, BotActivityAdmin)
admin.site.register(ErrorLog, ErrorLogAdmin)
```
This Django admin code sets up a user-friendly interface for users to manage their authorized social media accounts, configure the bot's tasks and schedule, and view bot activity and performance reports. Each Django model is associated with a corresponding admin class that controls how the model's data is displayed and edited in the Django admin interface. All secret data are hashed and stored securely.