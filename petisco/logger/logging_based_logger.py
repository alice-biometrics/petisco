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


class LoggingBasedLogger(ILogger):
    def __init__(
        self,
        logger_name: str,
        format: str = "%(name)s - %(levelname)s - %(message)s",
        config: Callable = None,
    ):
        PETISCO_LOGGING_LEVEL = os.environ.get("PETISCO_LOGGING_LEVEL", "INFO").upper()

        logging.basicConfig(format=format, level=PETISCO_LOGGING_LEVEL)
        if config:
            config()
        self.logger = logging.getLogger(logger_name)
        self.logger.info(f"Set PETISCO_LOGGING_LEVEL: {PETISCO_LOGGING_LEVEL}")

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
