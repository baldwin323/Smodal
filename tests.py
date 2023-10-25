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
    def setUp(self) -> None:
        self.bot = SocialMediaBot()
        self.sale_item = SaleItem()
        self.chat_bot = ChatBot()
        self.jwt_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRyaWFsIn0.eyJpc3MiOiJuZ2lueCBpc3N1ZXIiLCJpYXQiOjE2OTcyOTEwNDQsImp0aSI6IjE0ODM3Iiwic3ViIjoiVDAwMDEzMTk3NiIsImV4cCI6MTY5OTg4MzA0NH0.geiDEOEaxkk9naHlZI4pbBPRCChEJDKKLQSQebQeSfsn-uKk2fhqEEqUW3gLAN2r0j_uc2wgIlMgFPpDzmOf-1Nn6Dp54qfcUC8A2H59X7pkFhsaWRWGYPOn5peu3y8FPSo2a7gw77xOC2oz8o7iOhQYv4yb68bv2AWLepaGN0AsY4fr8tJykHrqmK6zN_1-85g9p-K50PzrEnHanO6WgmgSl6RxvCmIBlb6Hpeeb5bvm1kbsWgobpJSUXqepbJx5ef_YROGm93hVylnR80vCI53J-Ba0c6vJWrAec3sXmJQaDBjGYOl5mxueQWNz0cXNFd1RiimyIT3zmFSEePi71eatutmkZYVwR1mTgjGvJFCamZUWmeJ_o-N41l5I64_z-0sxIG9pjk8xC9EHhdqinikINcQ1s-jbTldG9aouDE8c9NG2jXumjV76CA6Xc3BD4-ciDLFIZrvbGX4H3dZgK141A6TUjnaO5AxP1UsDF1lLU-tE3vRMIxoR6VZzEKH"
 
        try:  
            self.pactflow_data = OIDCConfiguration.objects.first()
            self.pactflow_data.jwt_token = self.jwt_token
            self.pactflow_data.save()
            self.expected_headers = json.loads(self.pactflow_data.pactflow_response_headers)
            self.expected_body = json.loads(self.pactflow_data.pactflow_response_body)
        except Exception as e:
            logger.error(f'An error occurred during data fetching: {e}')

        if 'Local' in os.environ:
            self.bot.base_url = os.getenv('LOCAL_DB_URL')
            self.sale_item.base_url = os.getenv('LOCAL_DB_URL')
            self.chat_bot.base_url = os.getenv('LOCAL_DB_URL')
        
        self.build_commands = [["manage.py", "collectstatic", "--noinput"],
                            ["manage.py", "makemigrations"],
                            ["manage.py", "migration"]]

        self.user1 = User.objects.create_user(username='testuser1', password='12345') 
        login = self.client.login(username='testuser1', password='12345')   
        self.assertEqual(login, True) 

    def test_load_template(self):
        self.assertIsNotNone(self.bot.load_template('index.html'))

    def test_serve_page(self):
        self.assertIsNotNone(self.bot.serve_page('login'))
        
    def test_handle_function(self):
        self.assertEqual(self.bot.handle_function('index', 'request'), 'expected response')

    def test_building_commands(self):
        for command in self.build_commands:
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            self.assertEqual(process.returncode, 0, f"Command {command} failed with error: \n {stdout.decode('utf-8')} {stderr.decode('utf-8')}")

    def test_socialMediaBot(self):
        self.assertTrue(self.bot.check_connection())
        self.assertIsNotNone(self.bot.get_account_info())
        self.assertIsNotNone(self.bot.get_recent_posts())
        self.assertTrue(self.bot.post_status_update("Test Message"))

    def test_saleItem(self):
        self.assertEqual(self.sale_item.get_description(), "Sample Description")
        self.assertEqual(self.sale_item.get_price(), 1000)

    def test_chatBot(self):
        response = self.chat_bot.get_response("Hello?")
        self.assertIsNotNone(response)
        self.assertEqual(type(response), str)

    def test_affiliate_uploads(self):
        affiliate_upload = AffiliateUploads(upload_data = {'content': 'sample content'})
        affiliate_upload.save()
        saved_upload = AffiliateUploads.objects.first()
        self.assertIsNotNone(saved_upload)
        self.assertEqual(saved_upload.upload_data, {'content': 'sample content'})

    def test_openai_api_calls(self):
        openai_api_call = OpenAIAPICalls(call_details = {'api': 'sample api call'})
        openai_api_call.save()
        saved_call = OpenAIAPICalls.objects.first()
        self.assertIsNotNone(saved_call)
        self.assertEqual(saved_call.call_details, {'api': 'sample api call'})

    def test_dashboard(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/login', {'username':'testuser1', 'password':'12345'} )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 200)

    def test_form_submit(self):
        form_data = {"username": "testuser1", "password": "12345"}
        response = form_submit(HttpRequest().POST.update(form_data))
        self.assertEqual(response.status_code, 302)
        
    def test_file_upload(self):
        with open('test.txt', 'w') as file:
            test_file = FileUpload.objects.create(file=file.name)
            response = file_upload(test_file.id)
            self.assertEqual(response.status_code, 200)


    def test_user_activity(self):
        user_activity = UserActivity.objects.create(user_id=self.user1.id, activity="Test Activity", created_at="2022-02-28T20:00:00Z")
        response = user_activity(user_activity.id)
        self.assertEqual(response.status_code, 200)

    def test_banking(self):
        banking = Banking.objects.create(user_id=self.user1.id, transactions={"transaction1": "deposit $10"}, created_at="2022-02-28T20:00:00Z")
        response = banking(banking.id)
        self.assertEqual(response.status_code, 200)

    def test_user_auth(self):
        user_prof = UserProfile.objects.create(user_id=self.user1.id, birth_date="1985-05-12", image=None)
        self.assertIsNotNone(user_prof)
        self.assertEqual(user_prof.user_id, self.user1.id)
        self.assertEqual(user_prof.birth_date, "1985-05-12")
        self.assertEqual(user_prof.image, None)

    def test_handle_errors(self):
        with self.assertRaises(Exception):
            load_dashboard('fake_request')
        with self.assertRaises(Exception):
            login_user('fake_request')
        with self.assertRaises(Exception):
            logout_user('fake_request')
        with self.assertRaises(Exception):
            form_submit('fake_request')
        with self.assertRaises(Exception):
            file_upload('fake_request')
        with self.assertRaises(Exception):
            user_activity('fake_request')
        with self.assertRaises(Exception):
            banking('fake_request')
        with self.assertRaises(Exception):
            serve('fake_request', 'fake_page')