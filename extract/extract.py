import logging
from typing import List, Tuple

from configurations.models.app_model import AppConfig
from utils.function_utils import logger_extract, import_dynamic_function


@logger_extract
def extract(app_config: AppConfig, input_path: str) -> List[Tuple[str, bytes]]:
    logger = logging.getLogger(app_config.logger.logger_name)
    try:
        extraction_func = import_dynamic_function(
            package_name="extract",
            sub_package_name="strategies",
            module_name=app_config.extractor.strategy_module,
            function_name=app_config.extractor.extraction_function
        )
        return extraction_func(path=input_path)
    except FileNotFoundError as e:
        logger.error(f"File not found: {input_path}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while extracting data from {input_path}: {e}")
        raise e
