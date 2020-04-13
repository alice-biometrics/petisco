from abc import ABCMeta, abstractmethod
from typing import Any


class IApplication:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def get_app(self) -> Any:
        raise NotImplementedError
