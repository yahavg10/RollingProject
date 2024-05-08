import os
from typing import List, Tuple, Any, Callable

from main import app_config
from utils import import_dynamic_function
from utils.cache_utils import extract_file_hashes, is_md5_match, calculate_md5, update_cache
from utils.file_utils import extract_binary_file_content


def extract_binary_files(folder_path: str, extract_method: Callable[[str], Any]) -> List[Tuple[str, bytes]]:
    files_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            cached_hash, current_file_hash = extract_file_hashes(file_path, extract_method)
            file_binary = get_file_content(cached_hash, current_file_hash, extract_method, file_path)
            files_list.append((file_path, file_binary))
    return files_list


def get_file_content(cached_hash, current_file_hash, extract_method, file_path):
    if is_md5_match(cached_hash=cached_hash, current_hash=current_file_hash):
        file_binary = extract_method(file_path)
    else:
        file_binary = extract_binary_file_content(file_path)
        new_file_hash = calculate_md5(file_path)
        update_cache(load_method=import_dynamic_function(
            package_name=app_config.loader.package_name,
            sub_package_name=app_config.loader.sub_package_name,
            module_name=app_config.loader.strategy_module,
            function_name=app_config.loader.load_method
        ), cache_key=file_path, current_hash=new_file_hash)
    return file_binary
