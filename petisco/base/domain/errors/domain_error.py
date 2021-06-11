from abc import ABC, abstractmethod
from typing import Dict

from meiga import Error


class DomainError(ABC, Error):
    def __init__(self, uuid_value: str = None, additional_info: Dict[str, str] = None):
        self.uuid_value = uuid_value
        self.additional_info = additional_info
        self._set_message()

    def _set_message(self):
        self.message = ""

        if self.uuid_value:
            self.message += f" ({self.uuid_value})"

        if self.additional_info:
            self.message += f" [{self.additional_info}]"

    def get_message(self):
        return self.message

    @abstractmethod
    def detail(self) -> str:
        raise NotImplementedError

    def __str__(self):
        return self.detail()

    def __repr__(self):
        return self.detail()
