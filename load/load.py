import logging
from typing import NoReturn

from configurations.models.app_model import AppConfig
from utils.function_utils import logger_load, import_dynamic_function


@logger_load
def load(app_config: AppConfig, data) -> NoReturn:
    logger = logging.getLogger(app_config.logger.logger_name)
    try:
        loading_function = import_dynamic_function(package_name="load",
                                                   sub_package_name="strategies",
                                                   module_name=app_config.loader.strategy_module,
                                                   function_name=app_config.loader.loading_function)
        loading_function(data)
    except Exception as e:
        logger.error(f"An error occurred while loading data: {e}")
        raise e
