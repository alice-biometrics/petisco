from typing import Dict
from abc import ABCMeta, abstractmethod

from petisco.notifier.domain.notifier_message import NotifierMessage


class INotifier:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return f"INotifier"

    @abstractmethod
    def info(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def publish(self, notifier_message: NotifierMessage):
        raise NotImplementedError
