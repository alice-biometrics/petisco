from abc import abstractmethod

from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.base.misc.interface import Interface


class Notifier(Interface):
    @abstractmethod
    def publish(self, notifier_message: NotifierMessage):
        raise NotImplementedError
