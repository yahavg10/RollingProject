import importlib
import os

from configurations.models.app_model import AppConfig
from utils.file_utils import load_configuration
from utils.logger_utils import setup_custom_logger

app_config = load_configuration(config_model=AppConfig, path_to_load_from=os.getenv("conf_path"))
logger = setup_custom_logger(app_config.logger)


def logger_extract(func):
    def wrapped_function(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(f"extracted {len(result)} files")
        return result

    return wrapped_function


def logger_load(func):
    def wrapped_function(*args, **kwargs):
        result = func(*args, **kwargs)
        records = len(kwargs.get('data'))

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
