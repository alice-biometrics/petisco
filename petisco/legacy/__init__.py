# coding=utf-8
# Legacy module of petisco version 0

from petisco.legacy.logger.interface_logger import ILogger
from petisco.legacy.logger.log_message import LogMessage
from petisco.legacy.logger.logging_based_logger import LoggingBasedLogger

classes = ["ILogger", "LogMessage", "LoggingBasedLogger"]

# Constants
from petisco.legacy.logger.interface_logger import (
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    NOTSET,
    WARN,
    WARNING,
)

constants = ["CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"]

__all__ = classes + constants
