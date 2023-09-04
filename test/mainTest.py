import unittest
from flask import Flask
from flask.testing import FlaskClient
from modal.tokai.main import app

class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    # Testing response status
    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # Testing header values
    def test_headers(self):
        response = self.app.get('/')
        headers = response.headers
        self.assertIn('X-Replit-User-Id', headers)
        self.assertIn('X-Replit-User-Name', headers)
        self.assertIn('X-Replit-User-Roles', headers)
        self.assertIn('X-Replit-User-Bio', headers)
        self.assertIn('X-Replit-User-Profile-Image', headers)
        self.assertIn('X-Replit-User-Teams', headers)
        self.assertIn('X-Replit-User-Url', headers)

    # Testing header values for specific returned values
    def test_header_response_values(self):
        response = self.app.get('/')
        headers = response.headers
        self.assertEqual('MODALTOKAISAMPLE', headers['X-Replit-User-Name'])
        self.assertEqual('MODALTOKAISAMPLE', headers['X-Replit-User-Url'])

    # Testing functionality: 'clone' route
    def test_clone_post(self):
        data = {'prompt': 'test prompt', 'tokens': 100}
        response = self.app.post('/clone', data=json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)

    # Testing functionality: error handling 
    def test_error_handling(self):
        response = self.app.get('/an_invalid_route')
        self.assertEqual(500, response.status_code)

if __name__ == '__main__':
    unittest.main()