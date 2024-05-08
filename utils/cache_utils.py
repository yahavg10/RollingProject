from __future__ import annotations

import hashlib
import os
from typing import Callable, Any


def calculate_md5(file_path: str):
    # If the content of the file changes, the MD5 hash will change.
    # If only the file size or modification time changes,
    # but the content remains the same, the MD5 hash will remain unchanged.
    file_info = os.stat(file_path)
    file_info_str = f"{file_info.st_size}-{file_info.st_mtime}-{file_path}"
    md5_hash = hashlib.md5(file_info_str.encode())
    return md5_hash.hexdigest()


def update_cache(load_method: Callable[[str, str], Any], cache_key, current_hash):
    load_method(cache_key, current_hash)


def get_cached_hash(file_path, extract_method: Callable[[str], Any]):
    cache_key = f"{file_path}"
    cached_hash = extract_method(cache_key)
    return cached_hash


def extract_file_hashes(file_path, extract_method: Callable[[str], Any]):
    cached_hash = get_cached_hash(file_path, extract_method)
    current_file_hash = calculate_md5(file_path=file_path)
    return cached_hash, current_file_hash


def is_md5_match(cached_hash, current_hash):
    return cached_hash and cached_hash == current_hash
