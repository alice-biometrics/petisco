from petisco.base.application.notifier.notifier import Notifier
from petisco.base.application.notifier.notifier_message import NotifierMessage
from petisco.base.misc.builder import Builder


class NotImplementedNotifier(Notifier):
    def publish(self, message: NotifierMessage):
        pass


class NotImplementedNotifierBuilder(Builder):
    def build(self) -> NotImplementedNotifier:
        return NotImplementedNotifier()
