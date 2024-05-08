from enum import Enum

from pydantic import BaseModel, validator


class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class LoggerModel(BaseModel):
    logger_name: str
    base_level: LogLevel
    fmt: str
    datefmt: str
    debug_file_path: str
    info_file_path: str
    warning_file_path: str
    error_file_path: str
    critical_file_path: str

    @validator('base_level')
    def validate_base_level(cls, v):
        if v.upper() not in LogLevel.__members__:
            raise ValueError(
                f"Invalid log level: {v}. Valid levels are ', ({LogLevel.DEBUG}, {LogLevel.INFO} , {LogLevel.WARNING}, {LogLevel.ERROR}, {LogLevel.CRITICAL})")
        return v.upper()

