import hashlib
import importlib
import logging
import os
from datetime import datetime

import redis

from configurations.models.app_model import AppConfig
from utils.file_utils import load_configuration

app_config: AppConfig = load_configuration(config_model=AppConfig, path_to_load_from=os.getenv("conf_path"))
logger = logging.getLogger(app_config.logger.logger_name)


def logger_extract(func):
    def wrapped_function(*args, **kwargs):
        result = func(*args, **kwargs)
        records = len(result)
        is_empty(records, f"extracted {records} records from file", "!!Warning!! File is empty")

        return result

    return wrapped_function


def logger_load(func):
    def wrapped_function(*args, **kwargs):
        result = func(*args, **kwargs)
        records = len(kwargs.get('data'))
        is_empty(records, f"loaded {records} records to file", "!!Warning!! No Data to write")

        return result

    return wrapped_function


def import_dynamic_function(package_name: str, sub_package_name: str, module_name: str, function_name: str):
    try:
        full_module_path = f"{package_name}.{sub_package_name}.{module_name}"
        module = importlib.import_module(full_module_path)
        function = getattr(module, function_name)
        return function
    except AttributeError as e:
        logger.error(f"Function '{function_name}' not found in module '{module_name}'.")
        raise e
    except Exception as e:
        logger.error(e)
        raise e


def is_empty(param: int, info_msg: str, warn_msg: str):
    if param > 0:
        logger.info(f"{info_msg} {datetime.now().isoformat()}")
    else:
        logger.warning(f"{warn_msg} {datetime.now().isoformat()}")


def get_folder_hash(folder_path: str) -> str:
    hash_md5 = hashlib.md5()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hash_md5.update(chunk)
    return hash_md5.hexdigest()


def initialize_redis() -> redis.Redis:
    redis_client = redis.Redis(host=app_config.redis_config.host,
                               port=app_config.redis_config.port,
                               password=app_config.redis_config.password,
                               decode_responses=False)
    return redis_client
