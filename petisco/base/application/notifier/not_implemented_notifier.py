from petisco.base.application.notifier.notifier import Notifier
from petisco.base.application.notifier.notifier_exception_message import (
    NotifierExceptionMessage,
)
from petisco.base.application.notifier.notifier_message import NotifierMessage


class NotImplementedNotifier(Notifier):
    def publish(self, message: NotifierMessage):
        pass

    def publish_exception(self, notifier_exception_message: NotifierExceptionMessage):
        pass
