from typing import NoReturn

from configurations.models.app_model import AppConfig
from utils.function_utils import initialize_redis


def load_image_to_redis(app_config: AppConfig, images) -> NoReturn:
    redis_client = initialize_redis(app_config)
    for filename, content in images:
        redis_client.set(filename, content)
