import unittest
import json
from Smodal.digitalocean import get_droplets

class TestDigitalOcean(unittest.TestCase):

    def setUp(self):
        self.api_key = 'dop_v1_19b5e565d434cd27716aebb89e2f4f2d2ae90d9ef5b9f48616cfff819d8ec950'

    def test_get_droplets(self):
        droplets = get_droplets(self.api_key)
        # Checking if get_droplets returns a list
        self.assertIsInstance(droplets, list)

    def test_get_droplets_returns_success(self):
        """Test that the get_droplet function returns droplets on a successful API request."""
        droplets = get_droplets(self.api_key)
        # The API should return a list of droplets on successful request
        self.assertIsInstance(droplets, list)
        
    def test_droplet_structure(self):
        '''Test that the structure of each droplet is valid.'''
        droplets = get_droplets(self.api_key)
        for droplet in droplets: 
            # Check if the essential keys are in each droplet dict
            self.assertIn('id', droplet)
            self.assertIn('name', droplet)
            self.assertIn('status', droplet)
        
    def test_get_droplets_error(self):
        '''Test that get_droplet returns None on a non-200 response'''
        api_key = 'nonexistent_key'
        result = get_droplets(api_key)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()