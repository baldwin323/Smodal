import unittest
from Smodal import watch_page_modal as wpm

class TestWatchPageModal(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_open_pull_requests(self):
        result = wpm.get_open_pull_requests('repository name') # add your repository name here
		# For this test you can use any available open repository and target an open Pull Request.
		# Or can mock the request using python mock
        self.assertEqual(type(result), list, "Expected Result: list")

    def test_edit_pull_request(self):
        result = wpm.edit_pull_request('repository name', 1, "Test title") # Use your repository name, existing PR number and test title
        self.assertEqual(result.title, "Test title", "Expected Result: Test title")

    def test_home(self):
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_chat(self):
        response = client.get(reverse('chat'))
        self.assertEqual(response.status_code, 200)

    def test_takeover(self):
        response = client.get(reverse('takeover'))
        self.assertEqual(response.status_code, 200)

    def test_modal(self):
        response = wpm.modal('Any request') # here you need to entry a request, this will be depending on your setup,  
                                            # maybe you will need to mock this request
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()