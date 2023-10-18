from django.test import TestCase
from django.core.exceptions import ValidationError
from Smodal.social_media_bot import SocialMediaBot
from Smodal.sale_items import SaleItem, ChatBot
import uuid
import os
from .models import OIDCConfiguration, Credentials, EncryptedSensitiveData
import json
from subprocess import Popen, PIPE
from Smodal.logging import logger  # Import logging module

class SmodalTest(TestCase):
    def setUp(self) -> None:
        self.bot = SocialMediaBot()
        self.sale_item = SaleItem()
        self.chat_bot = ChatBot()
        try:  # Try to fetch the data, or log an exception
            self.pactflow_data = OIDCConfiguration.objects.first()
            self.expected_headers = json.loads(self.pactflow_data.pactflow_response_headers)
            self.expected_body = json.loads(self.pactflow_data.pactflow_response_body)
        except Exception as e:
            logger.error(f'An error occurred during data fetching: {e}')

        # Adjusting for local environment
        if 'Local' in os.environ:
            self.bot.base_url = os.getenv('LOCAL_DB_URL')
            self.sale_item.base_url = os.getenv('LOCAL_DB_URL')
            self.chat_bot.base_url = os.getenv('LOCAL_DB_URL')
        
        self.build_commands = [["./manage.py", "collectstatic", "--noinput"],
                            ["./manage.py", "makemigrations"],
                            ["./manage.py", "migrate"]]

    def test_build_commands(self):
        for command in self.build_commands:
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            self.assertEqual(process.returncode, 0, f"Command {command} failed with error: \n {stdout.decode('utf-8')} {stderr.decode('utf-8')}")
    
    # Rest of the test code...
    # ...
    # ...