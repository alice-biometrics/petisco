from abc import ABCMeta, abstractmethod

from petisco.logger.log_message import LogMessage

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0


class ILogger:

    __metaclass__ = ABCMeta

    @abstractmethod
    def log(self, logging_level: int, log_message: LogMessage):
        return NotImplementedError
