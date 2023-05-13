from petisco.extra.logger.log_message import LogMessage
from petisco.extra.logger.logger import (
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    NOTSET,
    WARN,
    WARNING,
    Logger,
)
from petisco.extra.logger.logging_based_logger import LoggingBasedLogger
from petisco.extra.logger.loguru_logger import LoguruLogger

classes = ["Logger", "LogMessage", "LoggingBasedLogger", "LoguruLogger"]
constants = ["CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"]

__all__ = classes + constants
