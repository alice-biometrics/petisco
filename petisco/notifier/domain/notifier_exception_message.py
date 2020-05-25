from typing import Dict

from dataclasses import dataclass

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.notifier.domain.notifier_message import NotifierMessage


@dataclass
class NotifierExceptionMessage(NotifierMessage):
    def __init__(
        self,
        function: str,
        exception: Exception,
        traceback: str,
        info_id: InfoId = None,
        info_petisco: Dict = None,
    ):
        super().__init__(info_id=info_id, info_petisco=info_petisco)
        self.function = function
        self.exception = exception
        self.traceback = traceback

    def __str__(self) -> str:
        return f"Error {self.function}: {repr(self.exception.__class__)} {self.exception} | {self.traceback}"
