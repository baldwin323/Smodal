```python
from django.test import TestCase
from .models import User, Platform, AccessToken, SocialMediaBot

class SocialMediaBotTestCase(TestCase):
    
    def setUp(self):
        self.bot = SocialMediaBot()
        self.user = User.objects.create(username='testuser', password='pwd')
        self.bot.add_user(self.user)
        
        # Creating a sample platform and access token
        self.platform = Platform.objects.create(name='testplatform')
        self.access_token = AccessToken.objects.create(token='testtoken', platform=self.platform, user=self.user)
        
    def test_post_message(self):
        result = self.bot.post_message(self.user.id, self.platform.name, 'Test Message')
        self.assertEqual(result, True, msg="Couldn't post the message.")

    def test_schedule_post(self):
        result = self.bot.schedule_post(self.user.id, self.platform.name, 'Test Message', '30/08/2030')
        self.assertEqual(result, True, msg="Couldn't schedule the post.")
        
    def test_monitor_keywords(self):
        result = self.bot.monitor_keywords(self.user.id, self.platform.name, 'keyword1, keyword2')
        self.assertEqual(result, True, msg="Keyword monitoring failed.")
        
    def test_engage(self):
        result = self.bot.engage(self.user.id, 'Like', 'Test Post')
        self.assertEqual(result, True, msg="Engagement failed.")
        
    def test_error_handling(self):
        # trying to authenticate a user who is not in database
        with self.assertRaises(Exception) as context:
            self.bot.authenticate("NonExistingUser")
        self.assertTrue('User not found' in str(context.exception))

        # trying to post a message using a platform which is not in database
        with self.assertRaises(Exception) as context:
            self.bot.post_message(self.user.id, 'NonExistingPlatform', 'Test Message')
        self.assertTrue('Platform not found' in str(context.exception))
    
    def tearDown(self):
        self.bot = None
        self.user.delete()
        self.platform.delete()
        self.access_token.delete()
```