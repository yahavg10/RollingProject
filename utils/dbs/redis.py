import redis as original_redis

from utils import app_config


class RedisSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.redis_instance = original_redis.Redis(*args, **kwargs)
        return cls._instance

    def __getattr__(self, name):
        return getattr(self.redis_instance, name)


redis_instance = RedisSingleton(host=app_config.redis_config.host,
                                port=app_config.redis_config.port,
                                password=app_config.redis_config.password,
                                decode_responses=False)


def get(key):
    redis_instance.get(key)


def set(key, value):
    redis_instance.set(key, value)
