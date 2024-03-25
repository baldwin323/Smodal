import unittest
from Smodal import error_pages
from unittest.mock import Mock

class TestErrorPages(unittest.TestCase):

    # Improving setup using setUpClass method for mocking objects used in multiple tests
    @classmethod
    def setUpClass(cls):
        cls.mock_request = Mock()
        cls.mock_exception = Mock()

    def test_handler404(self):
        response = error_pages.handler404(self.mock_request, self.mock_exception)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.template_name, '404.html')

    def test_handler500(self):
        response = error_pages.handler500(self.mock_request)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.template_name, '500.html')

    def test_handler404_content(self):
        response = error_pages.handler404(self.mock_request, self.mock_exception)
        self.assertEqual(response.context_data['error_code'], '404')
        self.assertEqual(response.context_data['error_message'], 'Page Not Found')

    def test_handler500_content(self):
        response = error_pages.handler500(self.mock_request)
        self.assertEqual(response.context_data['error_code'], '500')
        self.assertEqual(response.context_data['error_message'], 'Internal Server Error')

    def test_handler400(self):
        response = error_pages.handler400(self.mock_request, self.mock_exception)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.template_name, '400.html')

    def test_handler400_content(self):
        response = error_pages.handler400(self.mock_request, self.mock_exception)
        self.assertEqual(response.context_data['error_code'], '400')
        self.assertEqual(response.context_data['error_message'], 'Bad Request')

    # Adding test for handle_exception function in ErrorDetails class 
    def test_handle_exception(self):
        error_code, error_message = error_pages.handle_exception(exception=self.mock_exception, error_code=400)
        self.assertEqual(error_code, 400)
        self.assertEqual(error_message, 'Bad Request. The server could not understand the request.')

        error_code, error_message = error_pages.handle_exception(exception=self.mock_exception, error_code=404)
        self.assertEqual(error_code, 404)
        self.assertEqual(error_message, 'Page Not Found. The resource requested could not be found on the server.')

        error_code, error_message = error_pages.handle_exception(exception=self.mock_exception, error_code=500)
        self.assertEqual(error_code, 500)
        self.assertEqual(error_message, 'Internal Server Error. The server encountered an unexpected condition.')

if __name__ == '__main__':
    unittest.main()