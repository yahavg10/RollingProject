from __future__ import annotations

from typing import List, Tuple

import redis
import yaml

from utils.function_utils import get_folder_hash


def update_cache(redis_client: redis.StrictRedis, cache_key, current_hash, images):
    redis_client.set(cache_key, current_hash)
    redis_client.set(cache_key + ":images", yaml.dump(images))


def get_cache_parameters(folder_path, redis_client):
    cache_key = f"load_images:{folder_path}"
    cached_hash = redis_client.get(cache_key)
    current_hash = get_folder_hash(folder_path)
    return cache_key, cached_hash, current_hash


def is_folder_cache_match(current_hash, cached_hash) -> List[Tuple[str, bytes]] | None:
    return cached_hash and cached_hash == current_hash
