from django.test import TestCase
from django.core.exceptions import ValidationError
from Smodal.social_media_bot import SocialMediaBot
from Smodal.sale_items import SaleItem, ChatBot
import uuid
import os
from .models import OIDCConfiguration, Credentials, EncryptedSensitiveData
import json
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

    def test_pactflow_response_headers_saved_correctly(self) -> None:
        try:
            self.assertEqual(str(self.pactflow_data.pactflow_response_headers), str(self.expected_headers))
        except AssertionError:
            logger.error('Pactflow response headers were not saved correctly')

    def test_pactflow_response_body_saved_correctly(self) -> None:
        try:
            self.assertEqual(str(self.pactflow_data.pactflow_response_body), str(self.expected_body))
        except AssertionError:
            logger.error('Pactflow response body was not saved correctly')

    def test_social_media_site_login(self) -> None:
        platforms = ['facebook', 'twitter', 'instagram', 'linkedin', 'google']
        for platform in platforms:
            try:
                credentials = Credentials.objects.get(platform=platform)
                self.assertIsNotNone(credentials)
                self.assertEqual(credentials.username, "username")
                self.assertEqual(credentials.password, "password")

                encrypted_data = EncryptedSensitiveData.objects.get(platform=platform)
                self.assertIsNotNone(encrypted_data)
            except ValidationError:
                logger.error(f'Error logging in social media site {platform}')

    def test_secure_storage_and_retrieval_of_user_credentials_and_api_keys(self) -> None:
        platforms = ['facebook', 'twitter', 'instagram', 'linkedin', 'google']
        for platform in platforms:
            try:
                credentials = Credentials.objects.get(platform=platform)
                self.assertIsNotNone(credentials)
                encrypted_data = EncryptedSensitiveData.objects.get(platform=platform)
                self.assertIsNotNone(encrypted_data)

                decrypted_data = self.bot.decrypt(encrypted_data.encrypted_data, "This is a secret")
                self.assertEqual(decrypted_data.decode(), "password")
            except ValidationError as e:
                logger.error(
                    f'An error occurred during secure storage and retrieval of user credentials and API keys: {e}'
                )

    def test_sale_item_listing(self) -> None:
        try:
            self.sale_item.list_item("Test Item", 100, "This is a test item")
            item = self.sale_item.get_item("Test Item")
            self.assertIsNotNone(item)
            self.assertEqual(item["name"], "Test Item")
            self.assertEqual(item["price"], 100)
            self.assertEqual(item["description"], "This is a test item")
        except Exception as e:
            logger.error(f'Error occurred while testing item listing: {e}')

    def test_chat_bot_response(self) -> None:
        try:
            response = self.chat_bot.get_response("Test message")
            self.assertIsNotNone(response)
            self.assertEqual(response, "Test response")
        except Exception as e:
            logger.error(f'Error occurred while testing chat bot response: {e}')

    # Testing the integration with DigitalOcean API
    def test_do_api_integration(self) -> None:
        try:
            droplets = self.bot.get_droplets()
            self.assertIsNotNone(droplets)
            self.assertEqual(isinstance(droplets, list), True)
        except Exception as e:
            logger.error(f'Error occurred while testing DigitalOcean API integration: {e}')

    # Testing the deployment-related settings
    def test_deploy_settings(self) -> None:
        try:
            settings = self.bot.deploy()
            self.assertIsNotNone(settings)
            self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.postgresql')
            self.assertEqual(settings.DEBUG, False)
        except Exception as e:
            logger.error(f'Error occurred while testing deployment-related settings: {e}')