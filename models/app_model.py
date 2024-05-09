from typing import Type

from pydantic import BaseModel

from models.extractor_model import Extractor
from models.loader_model import Loader
from models.logger_model import LoggerModel
from models.redis_model import RedisModel


class Config(BaseModel):
    _instance = None

    def __new__(cls: Type["Config"], *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AppConfig(Config):
    redis_config: RedisModel
    extractor: Extractor
    loader: Loader
    logger: LoggerModel
