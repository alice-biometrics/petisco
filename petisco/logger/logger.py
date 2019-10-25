from abc import ABCMeta, abstractmethod


class Logger:

    __metaclass__ = ABCMeta

    @abstractmethod
    def log(self, logging_level: int, message: str):
        return NotImplementedError
