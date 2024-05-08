from __future__ import annotations

import logging
import os
from logging import Logger
from typing import *

import yaml
from pydantic import BaseModel

from configurations.models.app_model import AppConfig
from configurations.models.logger_model import LoggerModel


def extract_binary_file_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'rb') as f:
            content = f.read()
        images.append((filename, content))
    return images


def load_configuration(config_model: Union[Type[AppConfig], Type[BaseModel]], path_to_load_from: str) -> \
        Union[Type[AppConfig], Type[BaseModel]]:
    with open(file=path_to_load_from) as config_file:
        return config_model.validate(yaml.safe_load(config_file))


