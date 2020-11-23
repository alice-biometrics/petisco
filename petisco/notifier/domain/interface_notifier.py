from typing import Dict
from abc import ABCMeta, abstractmethod

from petisco.notifier.domain.notifier_message import NotifierMessage


class INotifier:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return f"INotifier"

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    @abstractmethod
    def publish(self, notifier_message: NotifierMessage):
        raise NotImplementedError
