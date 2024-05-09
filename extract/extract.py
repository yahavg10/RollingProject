from typing import List, Tuple

from configurations.models.extractor_model import Extractor

from utils import app_config, logger
from utils.function_utils import logger_extract, import_dynamic_function


@logger_extract
def extract(input_path: str) -> List[Tuple[str, bytes]]:
    try:
        extraction_func, extraction_helper_function = get_config_functions(app_config.extractor)
        return extraction_func(input_path, extraction_helper_function)
    except FileNotFoundError as e:
        logger.error(f"File not found: {input_path}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while extracting data from {input_path}: {e}")
        raise e


def get_config_functions(extractor_config: Extractor):
    extraction_func = import_dynamic_function(
        package_name="extract",
        sub_package_name="strategies",
        module_name="general",
        function_name=extractor_config.extraction_function
    )
    extract_method = import_dynamic_function(
        package_name=extractor_config.package_name,
        sub_package_name=extractor_config.sub_package_name,
        module_name=extractor_config.strategy_module,
        function_name=extractor_config.extract_method
    )
    return extraction_func, extract_method
