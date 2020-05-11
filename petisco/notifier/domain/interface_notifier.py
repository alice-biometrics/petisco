from typing import Dict
from abc import ABCMeta, abstractmethod


class INotifier:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return f"INotifier"

    @abstractmethod
    def info(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def publish(self, message: str):
        raise NotImplementedError
