import os

from models.app_model import AppConfig
from utils.cache_utils import calculate_md5, get_cached_hash, update_cache, is_md5_match
from utils.file_utils import load_configuration, extract_binary_file_content
from utils.function_utils import import_dynamic_function, logger_load, logger_extract
from utils.logger_utils import setup_custom_logger

app_config = load_configuration(config_model=AppConfig, path_to_load_from=os.getenv("conf_path"))
logger = setup_custom_logger(app_config.logger)
