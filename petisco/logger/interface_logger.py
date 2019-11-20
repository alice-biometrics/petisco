from abc import ABCMeta, abstractmethod

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
    def log(self, logging_level: int, message: str):
        return NotImplementedError
