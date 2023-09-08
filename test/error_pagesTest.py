import unittest
from Smodal import error_pages

class TestErrorPages(unittest.TestCase):

    def test_handler404(self):
        # Assumption that 'request' and 'exception' are properly initialized here
        response = error_pages.handler404(request, exception)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.template_name, '404.html')

    def test_handler500(self):
        # Assumption that 'request' is properly initialized here
        response = error_pages.handler500(request)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.template_name, '500.html')

if __name__ == '__main__':
    unittest.main()