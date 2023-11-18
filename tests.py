from django.test import TestCase
from django.core.exceptions import ValidationError
from Smodal.social_media_bot import SocialMediaBot
from Smodal.sale_items import SaleItem, ChatBot
from Smodal.lambda_functions import register_affiliate_manager, monitor_affiliated_models, give_credit
import uuid
import os
from .models import OIDCConfiguration, Credentials, EncryptedSensitiveData, AffiliateUploads, OpenAIAPICalls, UserProfile, FileUpload, Banking
from .views import load_dashboard, login_user, logout_user, form_submit, file_upload, user_activity, banking, serve
import json
from subprocess import Popen, PIPE
from Smodal.logging import logger 

class LambdaFunctionsTest(TestCase):
    def setUp(self) -> None:
        self.args = []
        self.kwargs = {}

    # Test the register_affiliate_manager lambda function
    def test_register_affiliate_manager(self):
        response = register_affiliate_manager(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    # Test the monitor_affiliated_models lambda function
    def test_monitor_affiliated_models(self):
        response = monitor_affiliated_models(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    # Test the give_credit lambda function
    def test_give_credit(self):
        response = give_credit(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')


class SmodalTest(TestCase):
   # existing tests...
  
    # Function to test the register_affiliate_manager lambda function
    def test_register_affiliate_manager(self):
        response = register_affiliate_manager(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    # Function to test the monitor_affiliated_models lambda function
    def test_monitor_affiliated_models(self):
        response = monitor_affiliated_models(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    # Function to test the give_credit lambda function
    def test_give_credit(self):
        response = give_credit(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    # Additional tests to handle error cases - To ensure compatibility with Python 3.12 and handle any exceptions that may arise due to the version upgrade
    # These tests check if correct exceptions are being handled when non-valid information is passed
    def test_handle_errors(self):
        # Testing load_dashboard with non-valid request
        with self.assertRaises(ValidationError):  # Using Django's ValidationError which is more specific
            load_dashboard('fake_request')

        # Testing login_user with non-valid request
        with self.assertRaises(ValidationError):  # Using Django's ValidationError which is more specific
            login_user('fake_request')

        # Testing logout_user with non-valid request
        with self.assertRaises(ValidationError):  # Using Django's ValidationError which is more specific
            logout_user('fake_request')

        # Testing form_submit with non-valid request
        with self.assertRaises(ValidationError):  # Using Django's ValidationError which is more specific
            form_submit('fake_request')

        # Testing file_upload with non-valid request
        with self.assertRaises(ValidationError):  # Using Django's ValidationError which is more specific
            file_upload('fake_request')

        # Testing user_activity with non-valid request
        with self.assertRaises(ValidationError):  # Using Django's ValidationError which is more specific
            user_activity('fake_request')

        # Testing banking with non-valid request
        with self.assertRaises(ValidationError):  # Using Django's ValidationError which is more specific
            banking('fake_request')

        # Testing serve with non-valid request and page
        with self.assertRaises(ValidationError):  # Using Django's ValidationError which is more specific
            serve('fake_request', 'fake_page')
