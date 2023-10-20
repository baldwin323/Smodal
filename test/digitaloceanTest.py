import unittest
import json
from Smodal.digitalocean import get_droplets

class TestDigitalOcean(unittest.TestCase):

    def setUp(self):
        self.api_key = 'dop_v1_19b5e565d434cd27716aebb89e2f4f2d2ae90d9ef5b9f48616cfff819d8ec950'

    def test_get_droplets(self):
        droplets = get_droplets(self.api_key)
        self.assertIsInstance(droplets, list)

if __name__ == '__main__':
    unittest.main()