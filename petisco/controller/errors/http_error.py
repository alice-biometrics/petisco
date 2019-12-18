from typing import Tuple

from abc import ABCMeta, abstractmethod


class HttpError:

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, message: str = "Unknown Error", code: int = 500):
        self.message = message
        self.code = code

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.code} | {self.message}"

    def handle(self) -> Tuple[dict, int]:
        return (
            {"error": {"type": self.__class__.__name__, "message": self.message}},
            self.code,
        )
