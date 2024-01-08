```python
import os
import unittest
from unittest.mock import patch
import Smodal.deploy as deploy

# AWS region
AWS_REGION = os.environ.get('AWS_REGION')

# Mocking responses for subprocess calls
COMMANDS = {
    'pip install awsebcli --upgrade --user': 0,
    'eb init': 0,
    'eb create': 0
}

def mock_run(args):
    cmd = ' '.join(args)
    if cmd in COMMANDS:
        return COMMANDS[cmd]
    else:
        raise ValueError(f"Command '{cmd}' not expected.")

# Unit Test Class
class TestDeploy(unittest.TestCase):

    # Mocking subprocess.run method
    @patch('subprocess.run', side_effect=mock_run)
    def test_install_ebcli(self, mock_run):
        deploy.install_ebcli()
        mock_run.assert_called_with(['pip', 'install', 'awsebcli', '--upgrade', '--user'])

    @patch('subprocess.run', side_effect=mock_run)
    def test_init_eb_environment(self, mock_run):
        deploy.init_eb_environment()
        mock_run.assert_called_with(['eb', 'init'])

    @patch('subprocess.run', side_effect=mock_run)
    def test_eb_deploy(self, mock_run):
        deploy.eb_deploy()
        mock_run.assert_called_with(['eb', 'create'])

    def test_create_dockerrun(self):
        deploy.create_dockerrun()
        with open('Dockerrun.aws.json', 'r') as file:
            content = file.read()

        expected_content = """
        {
            "AWSEBDockerrunVersion": "1",
            "Ports": [
                {
                    "ContainerPort": "8000"
                }
            ],
            "Volumes": [],
            "Logging": "/var/log/nginx"
        }
        """
        self.assertEqual(content, expected_content)

    def test_prepare_deployment_zip(self):
        deploy.prepare_deployment_zip()
        self.assertTrue(os.path.exists('eb_deployment.zip'))

# Defining main function for executing unit tests
if __name__ == '__main__':
    unittest.main()
```
These unit tests validate some of the important functions in the deploy.py script. We mock the subprocess calls to check if the correct commands are being called. Please make sure to use python -m unittest test/deployTest.py to run the tests.