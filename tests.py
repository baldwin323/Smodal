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

from .models import AIConversation, Banking, FileUpload, UserProfile, UIPageData

# Test cases related to Lambda functions and Smodal module
class LambdaFunctionsTest(TestCase):
    def setUp(self) -> None:
        self.args = []
        self.kwargs = {}

    def test_register_affiliate_manager(self):
        response = register_affiliate_manager(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    def test_monitor_affiliated_models(self):
        response = monitor_affiliated_models(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    def test_give_credit(self):
        response = give_credit(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')


class SmodalTest(TestCase):
    def test_register_affiliate_manager(self):
        response = register_affiliate_manager(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    def test_monitor_affiliated_models(self):
        response = monitor_affiliated_models(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    def test_give_credit(self):
        response = give_credit(*self.args, **self.kwargs)
        self.assertEqual(response, 'expected response')

    # Models test cases
    def test_user_profile_model(self):
        user_profile = UserProfile(birth_date='1990-01-01', image='test.jpg', preferences={"color": "blue"}, theme_preferences="dark")
        self.assertEqual(user_profile.birth_date, '1990-01-01')
        self.assertEqual(user_profile.image, 'test.jpg')
        self.assertEqual(user_profile.preferences, {"color": "blue"})
        self.assertEqual(user_profile.theme_preferences, 'dark')

    def test_file_upload_model(self):
        file_upload = FileUpload(file='test.pdf', token='random_string_here')
        self.assertEqual(file_upload.file, 'test.pdf')
        self.assertEqual(file_upload.token, 'random_string_here')

    def test_banking_model(self):
        banking = Banking(transactions={'id': '123', 'amount': '500'})
        self.assertEqual(banking.transactions, {'id': '123', 'amount': '500'})

    def test_ai_conversation_model(self):
        ai_conversation = AIConversation(user_id=1, previous_responses=['hi', 'hello'], current_context='greeting')
        self.assertEqual(ai_conversation.user_id, 1)
        self.assertEqual(ai_conversation.previous_responses, ['hi', 'hello'])
        self.assertEqual(ai_conversation.current_context, 'greeting')

    def test_ui_page_data_model(self):
        ui_page_data = UIPageData(page_id='dashboard', page_data={'title': 'Dashboard'})
        self.assertEqual(ui_page_data.page_id, 'dashboard')
        self.assertEqual(ui_page_data.page_data, {'title': 'Dashboard'})

    # Navigation test cases
    def test_ui_navigation(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    # Backend test cases
    def test_backend_functionality(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/api_serve/dashboard')
        self.assertEqual(response.status_code, 200)

    # Frontend/Angular test cases
    def test_frontend_functionality(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/app-root')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/app-root/handlePrevClick')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/app-root/handleNextClick')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/app-root/fetchData')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/app-root/onFileUpload')
        self.assertEqual(response.status_code, 200)

    # Docker service test cases
    def test_docker_compose_services(self):
        import docker
        client = docker.from_env()
        running_containers = client.containers.list()
        self.assertTrue(any("smodal-app" in s.name for s in running_containers))
        self.assertTrue(any("smodal-backend" in s.name for s in running_containers))
        self.assertTrue(any("smodal-frontend" in s.name for s in running_containers))