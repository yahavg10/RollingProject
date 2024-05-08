import logging

from configurations.models.logger_model import LoggerModel


def setup_custom_logger(logger_config: LoggerModel) -> logging.Logger:
    formatter = logging.Formatter(fmt=logger_config.fmt, datefmt=logger_config.datefmt)

    init_logger = logging.getLogger(name=logger_config.logger_name)
    init_logger.setLevel(logger_config.base_level)

    init_logger.addHandler(create_handler(handler_type="FileHandler",
                                          formatter=formatter,
                                          filename=logger_config.error_file_path))
    return init_logger


def create_handler(handler_type, formatter, **kwargs) -> logging.Handler:
    handler_mapping = {
        "FileHandler": logging.FileHandler,
        "StreamHandler": logging.StreamHandler,
    }

    handler_class = handler_mapping.get(handler_type)

    if handler_class:
        handler_class.setFormatter(formatter)
        return handler_class(**kwargs)
    else:
        raise ValueError("Unsupported handler type")
