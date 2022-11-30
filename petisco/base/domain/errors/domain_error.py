from typing import Dict, Optional

from meiga import Error


class DomainError(Error):
    """
    A base class to define Domain Errors
    """

    def __init__(
        self,
        uuid_value: Optional[str] = None,
        additional_info: Optional[Dict[str, str]] = None,
    ):
        self.uuid_value = uuid_value
        self.additional_info = additional_info
        self._additional_detail = ""
        self._specific_detail = "DomainError"
        self._set_detail()

    def _set_detail(self) -> None:
        if self.uuid_value:
            self._additional_detail += f" ({self.uuid_value})"

        if self.additional_info:
            self._additional_detail += f" [{self.additional_info}]"

    @classmethod
    def get_specify_detail(cls) -> str:
        return cls.__name__

    def detail(self) -> str:
        return f"{self.get_specify_detail()}{self._additional_detail}"

    def __str__(self) -> str:
        return f"{self.get_specify_detail()}{self._additional_detail}"

    def __repr__(self) -> str:
        return f"{self.get_specify_detail()}{self._additional_detail}"
