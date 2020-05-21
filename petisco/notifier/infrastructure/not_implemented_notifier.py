from typing import Dict

from petisco.notifier.domain.interface_notifier import INotifier


class NotImplementedNotifier(INotifier):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def publish(self, message: str):
        pass
