import os
import sys
import unittest
import pkg_resources
from unittest.mock import patch

from Smodal.manage import main as main_manage, handle_migrations, handle_execution, check_packages

class ManageTest(unittest.TestCase):

    def setUp(self):
        self.patches = []

    def tearDown(self):
        for patch in self.patches:
            patch.stop()

    def test_main(self):
        with patch('Smodal.manage.execute_from_command_line') as execute_from_command_line_mocked:
            main_manage()
            execute_from_command_line_mocked.assert_any_call(['./manage.py', 'makemigrations'])
            execute_from_command_line_mocked.assert_any_call(['./manage.py', 'migrate'])
            execute_from_command_line_mocked.assert_called_with(sys.argv)

    def test_handle_migrations(self):
        with patch('Smodal.manage.execute_from_command_line') as execute_from_command_line_mocked:
            handle_migrations(False)
            execute_from_command_line_mocked.assert_any_call(['./manage.py', 'makemigrations'])
            execute_from_command_line_mocked.assert_called_with(['./manage.py', 'migrate'])

    def test_handle_execution(self):
        with patch('Smodal.manage.execute_from_command_line') as execute_from_command_line_mocked:
            handle_execution(False)
            execute_from_command_line_mocked.assert_called_with(sys.argv)

    def test_check_packages(self):
        required_packages = ['numpy', 'replit', 'Django', 'urllib3', 'requests', 'bootstrap4',
                             'pytest', 'pytest-django', 'django-debug-toolbar', 'logging', 'caching',
                             'django-allauth', 'django-crispy-forms', 'django-environ']
        installed_packages = [pkg.key for pkg in pkg_resources.working_set]

        for package in required_packages:
            self.assertIn(package, installed_packages)

if __name__ == '__main__':
    unittest.main()