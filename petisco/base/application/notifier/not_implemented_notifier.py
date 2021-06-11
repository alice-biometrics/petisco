from petisco.base.application.notifier.notifier import Notifier
from petisco.base.application.notifier.notifier_message import NotifierMessage


class NotImplementedNotifier(Notifier):
    def publish(self, message: NotifierMessage):
        pass
