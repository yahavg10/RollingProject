import logging

from models.logger_model import LoggerModel


def setup_custom_logger(logger_config: LoggerModel) -> logging.Logger:
    formatter = logging.Formatter(fmt=logger_config.fmt, datefmt=logger_config.datefmt)

    init_logger = logging.getLogger(name=logger_config.logger_name)
    init_logger.setLevel(logger_config.base_level)
    for handler_name in logger_config.handlers:
        handler = create_handler(handler_name=handler_name,
                                 filename=logger_config.log_file_path)
        handler.setFormatter(formatter)
        init_logger.addHandler(handler)
    return init_logger


def create_handler(handler_name, **kwargs) -> logging.Handler:
    handler_mapping = {
        "FileHandler": logging.FileHandler,
        "StreamHandler": logging.StreamHandler,
    }

    handler_class = handler_mapping.get(handler_name)
    if handler_class:
        if handler_name == "StreamHandler":
            kwargs.pop("filename")
            return handler_class(**kwargs)
        else:
            return handler_class(**kwargs)
    else:
        raise ValueError("Unsupported handler type")
