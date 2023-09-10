import unittest
from Smodal import error_pages
from unittest.mock import Mock

class TestErrorPages(unittest.TestCase):

    def setUp(self):
        self.mock_request = Mock()

    def test_handler404(self):
        exception = Mock()
        response = error_pages.handler404(self.mock_request, exception)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.template_name, '404.html')

    def test_handler500(self):
        response = error_pages.handler500(self.mock_request)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.template_name, '500.html')

    def test_handler404_content(self):
        exception = Mock()
        response = error_pages.handler404(self.mock_request, exception)
        self.assertEqual(response.context_data['error_code'], '404')
        self.assertEqual(response.context_data['error_message'], 'Page Not Found')

    def test_handler500_content(self):
        response = error_pages.handler500(self.mock_request)
        self.assertEqual(response.context_data['error_code'], '500')
        self.assertEqual(response.context_data['error_message'], 'Internal Server Error')

if __name__ == '__main__':
    unittest.main()