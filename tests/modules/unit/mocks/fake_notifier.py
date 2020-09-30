from typing import Dict

from petisco.notifier.domain.interface_notifier import INotifier
from petisco.notifier.domain.notifier_message import NotifierMessage


class FakeNotifier(INotifier):
    def __init__(self):
        self.publish_called = False
        self.publish_times_called = 0

    def info(self) -> Dict:
        pass

    def publish(self, notifier_message: NotifierMessage):
        self.publish_called = True
        self.publish_times_called += 1
