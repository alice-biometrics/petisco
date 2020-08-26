import logging
import os
from typing import Callable

from petisco.logger.log_message import LogMessage
from petisco.logger.interface_logger import (
    ILogger,
    INFO,
    ERROR,
    WARN,
    WARNING,
    DEBUG,
    CRITICAL,
    FATAL,
)

CORRESPONDENCES_LOGGING_LEVEL = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class LoggingBasedLogger(ILogger):
    def __init__(
        self,
        logger_name: str,
        format: str = "%(name)s - %(levelname)s - %(message)s",
        config: Callable = None,
    ):
        self.logging_level = os.environ.get("PETISCO_LOGGING_LEVEL", "INFO").upper()
        logging_level_value = CORRESPONDENCES_LOGGING_LEVEL.get(
            self.logging_level, logging.INFO
        )
        logging.basicConfig(format=format, level=logging_level_value)
        if config:
            config()
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging_level_value)
        self.logger.info(f"Set PETISCO_LOGGING_LEVEL: {self.logging_level}")

    def log(self, logging_level, log_message: LogMessage):
        message = log_message.to_dict()
        if logging_level == INFO:
            message["meta"]["level"] = "info"
            self.logger.info(message)
        elif logging_level == DEBUG:
            message["meta"]["level"] = "debug"
            self.logger.debug(message)
        elif logging_level == CRITICAL:
            message["meta"]["level"] = "critical"
            self.logger.critical(message)
        elif logging_level == FATAL:
            message["meta"]["level"] = "fatal"
            self.logger.fatal(message)
        elif logging_level == ERROR:
            message["meta"]["level"] = "error"
            self.logger.error(message)
        elif logging_level == WARN:
            message["meta"]["level"] = "warning"
            self.logger.warn(message)
        elif logging_level == WARNING:
            message["meta"]["level"] = "warning"
            self.logger.warning(message)
