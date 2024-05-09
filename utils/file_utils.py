from __future__ import annotations

from typing import *

import yaml
from pydantic import BaseModel

from models.app_model import AppConfig


def extract_binary_file_content(file_path): return open(file_path, 'rb').read()


def load_configuration(config_model: Union[Type[AppConfig], Type[BaseModel]], path_to_load_from: str) -> \
        Union[Type[AppConfig], Type[BaseModel]]:
    with open(file=path_to_load_from) as config_file:
        return config_model.validate(yaml.safe_load(config_file))
