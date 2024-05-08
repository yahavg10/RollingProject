import os
from typing import NoReturn

os.environ["conf_path"] = "configurations/base.yml"

from configurations.models.app_model import AppConfig
from extract.extract import extract
from load.load import load
from utils.file_utils import load_configuration, setup_custom_logger


def program() -> NoReturn:
    logger = None
    try:
        app_config: AppConfig = load_configuration(config_model=AppConfig, path_to_load_from=os.getenv("conf_path"))

        logger = setup_custom_logger(app_config.logger)
        load(data=extract(app_config=app_config, input_path=app_config.extractor.input_path),
             app_config=app_config)
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    program()
