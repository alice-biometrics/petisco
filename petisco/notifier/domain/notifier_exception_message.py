from dataclasses import dataclass

from petisco.notifier.domain.notifier_message import NotifierMessage


@dataclass
class NotifierExceptionMessage(NotifierMessage):
    def __init__(self, function: str, exception: Exception, traceback: str):
        self.function = function
        self.exception = exception
        self.traceback = traceback
        super().__init__()

    def __str__(self) -> str:
        return f"Error {self.fucntion}: {repr(self.exception.__class__)} {self.exception} | {self.traceback}"
