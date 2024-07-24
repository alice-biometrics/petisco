import os

from loguru import logger

from petisco.extra.logger.log_message import LogMessage
from petisco.extra.logger.logger import (
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    WARN,
    WARNING,
    Logger,
)


class LoguruLogger(Logger):
    def __init__(self) -> None:
        self.logging_level = os.environ.get("PETISCO_LOGGING_LEVEL", "INFO").upper()
        logger.info(f"Set PETISCO_LOGGING_LEVEL: {self.logging_level}")

    def log(self, logging_level, log_message: LogMessage) -> None:
        message = log_message.to_dict()
        if logging_level == INFO:
            message["meta"]["level"] = "info"
            logger.info(message)
        elif logging_level == DEBUG:
            message["meta"]["level"] = "debug"
            logger.debug(message)
        elif logging_level == CRITICAL:
            message["meta"]["level"] = "critical"
            logger.critical(message)
        elif logging_level == FATAL:
            message["meta"]["level"] = "fatal"
            logger.error(message)
        elif logging_level == ERROR:
            message["meta"]["level"] = "error"
            logger.error(message)
        elif logging_level in (WARN, WARNING):
            message["meta"]["level"] = "warning"
            logger.warning(message)
