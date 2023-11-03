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
        # Call the function once, this should set the value in cache
        self.assertEqual(self.cache_test_function(), self.cache_value)
        self.assertIn(self.cache_key, cache)

        # Call again, this should fetch result from cache and be same
        self.assertEqual(self.cache_test_function(), self.cache_value)

        # Clear cache and check if the function still produces consistent results after cache is cleared
        cache.clear()
        self.assertEqual(self.cache_test_function(), self.cache_value)

    def test_cache_decorator(self):
        # Verifying that function result is cached
        result = self.cache_test_function()
        self.assertIn(self.cache_key, cache)
        self.assertEqual(result, cache.get(self.cache_key))

        # Clear cache and check if the function still produces consistent results
        cache.clear()
        self.assertEqual(self.cache_test_function(), self.cache_value)

        # Verify again that result is not from cache, but function
        result = self.cache_test_function()
        self.assertNotEqual(result, cache.get(self.cache_key))

    def test_fail_to_cache(self):
        # Test case where caching fails intentionally
        with self.assertRaises(Exception) as context:
            @cache_result(bad_cache_key)
            def bad_cache_function(self):
                return self.cache_value

        self.assertTrue('An error occurred while fetching from cache or setting result into cache' in context.exception)

if __name__ == "__main__":
    # Load and run the unit tests
    unittest.main()