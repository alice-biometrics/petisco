import logging
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
        logging_level=logging.INFO,
        format: str = "%(name)s - %(levelname)s - %(message)s",
        config: Callable = None,
    ):

        logging.basicConfig(format=format, level=logging_level)
        if config:
            config()
        self.logger = logging.getLogger(logger_name)

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
