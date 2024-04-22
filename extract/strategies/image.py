import os
from typing import List, Tuple

import redis

from configurations.models.app_model import AppConfig
from utils.cache_utils import is_folder_cache_match, get_cache_parameters, update_cache
from utils.file_utils import read_from_file, extract_images_from_folder
from utils.function_utils import initialize_redis


def extract_images(app_config: AppConfig, path: str) -> List[Tuple[str, bytes]]:
    redis_client = initialize_redis(app_config)
    cache_key, cached_hash, current_hash = get_cache_parameters(path, redis_client)
    images = []
    if is_folder_cache_match(cached_hash=cached_hash,
                             current_hash=current_hash):
        images = redis_client.get(cache_key + ":images")
    else:
        images = extract_images_from_folder(path)
        update_cache(redis_client=redis_client, cache_key=cache_key, current_hash=current_hash, images=images)
    return images



