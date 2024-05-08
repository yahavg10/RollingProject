import os
from typing import NoReturn

os.environ["conf_path"] = "configurations/base.yml"

from utils import app_config, logger
from extract.extract import extract
from load.load import load


def main() -> NoReturn:
    try:
        extracted_data = extract(input_path=app_config.extractor.input_path)
        load(data=extracted_data)
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    main()
