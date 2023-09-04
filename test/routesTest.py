import unittest
import flask
from Smodal import routes
from flask import request
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = flask.Flask(__name__)
        self.client = FlaskClient(self.app, self)
        self.routes = routes

    def tearDown(self):
        pass

    def test_api_request(self):
        with self.client.session_transaction() as session:
            session['apiName'] = routes.API_NAME
        response = self.client.post('/api')
        self.assertEqual(response.status_code, 200)
    
    def test_upload_file(self):
        data = {
            'file': (BytesIO(b'content'), 'test.txt')
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File successfully uploaded', response.data)

    def test_get_file(self):
        test_id = 'test_id' 
        response = self.client.get('/files/'+test_id)
        if response.status_code == 200:
            self.assertIn('File', response.data)
        else:
            self.assertIn(b'File not found!', response.data)

    def test_missing_request_cases(self):
        response = self.client.post('/api')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid API name!', response.data)
        
        response = self.client.post('/upload')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No file part', response.data)

        response = self.client.get('/files/')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()