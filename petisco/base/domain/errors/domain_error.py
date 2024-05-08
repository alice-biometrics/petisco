from typing import Dict, Optional

from deprecation import deprecated
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

    def set_additional_info(self, info: Optional[Dict[str, str]]) -> None:
        if self.additional_info:
            self.additional_info = dict(self.additional_info, **info)
        else:
            self.additional_info = info

    @classmethod
    @deprecated("get_specify_detail is deprecated. Use the `get_specific_detail` instead.")
    def get_specify_detail(cls) -> str:
        return cls.get_specific_detail()

    @classmethod
    def get_specific_detail(cls) -> str:
        return cls.__name__

    def detail(self) -> str:
        return f"{self.get_specific_detail()}{self._additional_detail}"

    def __str__(self) -> str:
        return f"{self.get_specific_detail()}{self._additional_detail}"

    def __repr__(self) -> str:
        return f"{self.get_specific_detail()}{self._additional_detail}"
