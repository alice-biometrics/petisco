from petisco.legacy.notifier.domain.notifier_message import NotifierMessage


class NotifierExceptionMessage(NotifierMessage):
    executor: str
    exception: Exception
    traceback: str
    input_parameters: dict = None
