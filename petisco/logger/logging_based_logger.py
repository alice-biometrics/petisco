import logging
from typing import Callable

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
        config_func: Callable = None,
    ):

        logging.basicConfig(format=format, level=logging_level)
        if config_func:
            config_func()
        self.logger = logging.getLogger(logger_name)

    def log(self, logging_level, message):
        if logging_level == INFO:
            self.logger.info(message)
        elif logging_level == DEBUG:
            self.logger.debug(message)
        elif logging_level == CRITICAL:
            self.logger.critical(message)
        elif logging_level == FATAL:
            self.logger.fatal(message)
        elif logging_level == ERROR:
            self.logger.error(message)
        elif logging_level == WARN:
            self.logger.warn(message)
        elif logging_level == WARNING:
            self.logger.warning(message)
