import unittest
from django.test import RequestFactory
from Smodal.html_template_util import navbar_view, footer_view, modal_view, other_page_view

class TestHtmlTemplateUtil(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_navbar_view(self):
        request = self.factory.get('/navbar')
        response = navbar_view(request)
        self.assertEqual(response.status_code, 200)

    def test_footer_view(self):
        request = self.factory.get('/footer')
        response = footer_view(request)
        self.assertEqual(response.status_code, 200)

    def test_modal_view(self):
        request = self.factory.get('/modal')
        response = modal_view(request)
        self.assertEqual(response.status_code, 200)

    def test_other_page_view(self):
        request = self.factory.get('/other_page')
        response = other_page_view(request)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()