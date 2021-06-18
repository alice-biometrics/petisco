from typing import Dict

from petisco.legacy.notifier.domain.interface_notifier import INotifier
from petisco.legacy.notifier.domain.notifier_message import NotifierMessage


class NotImplementedNotifier(INotifier):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def publish(self, message: NotifierMessage):
        pass
