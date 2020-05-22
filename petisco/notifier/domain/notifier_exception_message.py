from dataclasses import dataclass

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.notifier.domain.notifier_message import NotifierMessage


@dataclass
class NotifierExceptionMessage(NotifierMessage):
    def __init__(
        self, function: str, exception: Exception, traceback: str, info_id: InfoId
    ):
        self.function = function
        self.exception = exception
        self.traceback = traceback
        self.info_id = info_id
        super().__init__()

    def __str__(self) -> str:
        return f"Error {self.function}: {repr(self.exception.__class__)} {self.exception} | {self.traceback}"
