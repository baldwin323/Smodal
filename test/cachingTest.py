import unittest
from Smodal.caching import cache_result
from django.core.cache import cache

class TestCacheResult(unittest.TestCase):

    def setUp(self):
        self.cache_key = "test_key"
        self.cache_value = "cached_value"
        cache.clear()

    @cache_result(self.cache_key)
    def cache_test_function(self):
        return self.cache_value

    def test_cache_result(self):
        # Call the function once, this will set the value in cache
        self.assertEqual(self.cache_test_function(), self.cache_value)

        # Verify the value is present in cache
        self.assertIn(self.cache_key, cache)

        # Call again, this time result should come from cache and still be same
        self.assertEqual(self.cache_test_function(), self.cache_value)

        # Clear cache and check if the function still produces consistent results
        cache.clear()
        self.assertEqual(self.cache_test_function(), self.cache_value)

if __name__ == "__main__":
    # Load and run the unit tests
    unittest.main()