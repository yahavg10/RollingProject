import unittest
from unittest.mock import MagicMock

from your_module import get, set, redis_instance


class TestRedisFunctions(unittest.TestCase):

    def test_get_givenKey_callsRedisGetWithKey(self):
        # Test get function calls redis_instance.get with the given key
        key = "test_key"
        redis_instance.get = MagicMock()
        get(key)
        redis_instance.get.assert_called_once_with(key)

    def test_set_givenKeyAndValue_callsRedisSetWithKeyAndValue(self):
        # Test set function calls redis_instance.set with the given key and value
        key = "test_key"
        value = "test_value"
        redis_instance.set = MagicMock()
        set(key, value)
        redis_instance.set.assert_called_once_with(key, value)

    def test_set_givenKeyAndValue_setsCorrectValueInRedis(self):
        # Test set function sets the correct value in the Redis instance
        key = "test_key"
        value = "test_value"
        set(key, value)
        # Check if the value was set correctly by getting the value from Redis
        self.assertEqual(redis_instance.get(key), value)
