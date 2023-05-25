from abc import ABC, abstractmethod

from petisco.extra.logger.log_message import LogMessage

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


class Logger(ABC):
    @abstractmethod
    def log(self, logging_level: int, log_message: LogMessage):
        return NotImplementedError
