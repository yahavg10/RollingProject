from __future__ import annotations

import logging
from logging import Logger
import os
from typing import *

import yaml
from pydantic import BaseModel

from configurations.models.app_model import AppConfig
from configurations.models.logger_model import LoggerModel


def extract_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'rb') as f:
            content = f.read()
        images.append((filename, content))
    return images


def read_from_file(file_path: str,
                   file_reader: Callable[[TextIO], Optional[Dict[str, Any]]],
                   mode: str = 'r', encode: str = 'utf-8', newline: str = '') -> Any:
    with open(file=file_path, mode=mode, newline=newline, encoding=encode) as file:
        return file_reader(file)


def load_configuration(config_model: Union[Type[AppConfig], Type[BaseModel]], path_to_load_from: str) -> Any:
    return config_model.validate(read_from_file(file_path=path_to_load_from, file_reader=yaml.safe_load))


app_config: AppConfig = load_configuration(config_model=AppConfig,
                                           path_to_load_from=os.getenv("conf_path"))

logger = logging.getLogger(app_config.logger.logger_name)


def setup_custom_logger(name, logger_config: LoggerModel, log_level=logging.DEBUG) -> Logger:
    formatter = logging.Formatter(fmt=logger_config.fmt, datefmt=logger_config.datefmt)

    init_logger = logging.getLogger(name)
    init_logger.setLevel(log_level)

    set_debug_handler(formatter, log_level, init_logger, logger_config)

    set_info_handler(formatter, log_level, init_logger, logger_config)

    set_warning_handler(formatter, log_level, init_logger, logger_config)

    set_error_handler(formatter, log_level, init_logger, logger_config)

    set_critical_handler(formatter, log_level, init_logger, logger_config)

    return init_logger


def set_debug_handler(formatter, log_level, logger, logger_config):
    if log_level >= logging.DEBUG:
        handler_debug = logging.FileHandler(logger_config.debug_file_path)
        handler_debug.setLevel(logging.DEBUG)
        handler_debug.setFormatter(formatter)
        logger.addHandler(handler_debug)


def set_info_handler(formatter, log_level, logger, logger_config):
    if log_level >= logging.INFO:
        handler_info = logging.FileHandler(logger_config.info_file_path)
        handler_info.setLevel(logging.INFO)
        handler_info.setFormatter(formatter)
        logger.addHandler(handler_info)


def set_warning_handler(formatter, log_level, logger, logger_config):
    if log_level >= logging.WARNING:
        handler_warning = logging.FileHandler(logger_config.warning_file_path)
        handler_warning.setLevel(logging.WARNING)
        handler_warning.setFormatter(formatter)
        logger.addHandler(handler_warning)


def set_error_handler(formatter, log_level, logger, logger_config):
    if log_level >= logging.ERROR:
        handler_error = logging.FileHandler(logger_config.error_file_path)
        handler_error.setLevel(logging.ERROR)
        handler_error.setFormatter(formatter)
        logger.addHandler(handler_error)


def set_critical_handler(formatter, log_level, logger, logger_config):
    if log_level >= logging.CRITICAL:
        handler_critical = logging.FileHandler(logger_config.critical_file_path)
        handler_critical.setLevel(logging.CRITICAL)
        handler_critical.setFormatter(formatter)
        logger.addHandler(handler_critical)
