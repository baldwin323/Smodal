import unittest
import flask
from Smodal import routes
from flask import request
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage
from io import BytesIO

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        self.client = FlaskClient(self.app, self)
        self.routes = routes

    def tearDown(self):
        pass

    # Test for valid API requests.
    def test_api_request(self):
        with self.client.session_transaction() as session:
            session['apiName'] = routes.API_NAME
        response = self.client.post('/api')
        self.assertEqual(response.status_code, 200)

    # Test for invalid API requests.
    def test_invalid_api(self):
        response = self.client.post('/api', data={'apiName': 'invalidApi'})
        self.assertEqual(response.status_code, 400)

    # Test for valid file uploads.
    def test_upload_file(self):
        data = {
            'file': (BytesIO(b'content'), 'test.txt')
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File successfully uploaded', response.data)

    # Test for uploads without files.
    def test_upload_without_file(self):
        response = self.client.post('/upload', data={}, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    # Test for valid file retrieval.
    def test_get_file(self):
        test_id = 'test_id' 
        response = self.client.get('/files/'+test_id)
        if response.status_code == 200:
            self.assertIn('File', response.data)
        else:
            self.assertIn(b'File not found!', response.data)

    # Test for invalid request cases.
    def test_missing_request_cases(self):
        response = self.client.post('/api')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid API name!', response.data)
        
        response = self.client.post('/upload')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file part', response.data)

        response = self.client.get('/files/')
        self.assertEqual(response.status_code, 404)

    # Additional tests for routes.py functions.

    # Test for valid session creation.
    def test_session_creation(self):
        with self.client.session_transaction() as session:
            session['session'] = 'test_session' 
        response = self.client.get('/session')
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_session', response.data.decode())

    # Test for invalid session retrieval.
    def test_invalid_session(self):
        response = self.client.get('/session')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid session!', response.data)

if __name__ == '__main__':
    unittest.main()