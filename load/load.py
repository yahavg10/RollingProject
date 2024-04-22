import logging

from configurations.models.app_model import AppConfig
from utils.function_utils import logger_load, import_dynamic_function


@logger_load
def load(app_config: AppConfig, data):
    logger = logging.getLogger(app_config.logger.logger_name)
    try:
        loading_function = import_dynamic_function(package_name="load",
                                                   sub_package_name="strategies",
                                                   module_name=app_config.loader.strategy_module,
                                                   function_name=app_config.loader.loading_function)
        loading_function(app_config, data)
    except Exception as e:
        logger.error(f"An error occurred while loading data: {e}")
        raise e
