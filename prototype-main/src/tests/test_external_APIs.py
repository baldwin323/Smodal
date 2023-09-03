import unittest
import sys
sys.path.append('/Smodal/prototype-main/src')
import external_APIs

class TestExternalAPIs(unittest.TestCase):

    def setUp(self):
        self.location = "San Francisco"
        self.topic = "technology"

    def test_fetch_weather(self):
        data = external_APIs.fetch_weather(self.location)
        self.assertIsInstance(data, dict)
        self.assertTrue('main' in data)
        self.assertTrue('temp' in data['main'])
        self.assertTrue('weather' in data)

    def test_fetch_news(self):
        data = external_APIs.fetch_news(self.topic)
        self.assertIsInstance(data, dict)
        self.assertTrue('articles' in data)

if __name__ == "__main__":
    unittest.main()