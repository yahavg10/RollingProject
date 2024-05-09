import logging
from typing import NoReturn

from configurations.models.loader_model import Loader

from utils import app_config
from utils.function_utils import logger_load, import_dynamic_function


@logger_load
def load(data) -> NoReturn:
    logger = logging.getLogger(app_config.logger.logger_name)
    try:
        loading_function, load_method = get_config_functions(app_config.loader)
        loading_function(data, load_method)
    except Exception as e:
        logger.error(f"An error occurred while loading data: {e}")
        raise e


def get_config_functions(loader_config: Loader):
    loading_func = import_dynamic_function(
        package_name="load",
        sub_package_name="strategies",
        module_name="general",
        function_name=loader_config.loading_function
    )
    load_method = import_dynamic_function(
        package_name=loader_config.package_name,
        sub_package_name=loader_config.sub_package_name,
        module_name=loader_config.strategy_module,
        function_name=loader_config.load_method
    )
    return loading_func, load_method
