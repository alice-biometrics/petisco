import inspect
import re

from meiga import Error

from petisco.domain.errors.length_limit_string_value_object_error import (
    ExceedLengthLimitValueObjectError,
    NotReachMinimumValueObjectError,
    NotHasSpecificLengthValueObjectError,
)
from petisco.domain.value_objects.value_object import ValueObject


class InvalidStringValueObjectError(Error):
    def __init__(self, message):
        self.message = message


class StringValueObject(ValueObject):
    def __init__(self, value: str):
        self.value = value
        super(StringValueObject, self).__init__()

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return f"[{self.__class__.__name__}: {self.value}]"

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(
            self.__class__, other.__class__
        ):
            return self.value == other.value
        else:
            return False

    def _raise_error(self, raise_cls):
        if "message" in inspect.getfullargspec(raise_cls).args:
            raise raise_cls(message=self.value)
        else:
            raise raise_cls()

    def _ensure_value_contains_valid_char(
        self, raise_cls=InvalidStringValueObjectError, allow_utf8mb4: bool = True
    ):
        if not isinstance(self.value, str) or not re.search(
            r"^[\w\s\-,.']*$", self.value
        ):
            self._raise_error(raise_cls)
        if not allow_utf8mb4:
            if not all(
                [
                    re.match("[^\u0000-\uffff]", char) is None
                    for char in list(self.value)
                ]
            ):
                self._raise_error(raise_cls)

    def _ensure_value_is_less_than_n_char(
        self, max_num_chars: int, raise_cls=ExceedLengthLimitValueObjectError
    ):
        if len(self.value) > max_num_chars:
            self._raise_error(raise_cls)

    def _ensure_value_is_greater_than_n_char(
        self, max_num_chars: int, raise_cls=NotReachMinimumValueObjectError
    ):
        if len(self.value) < max_num_chars:
            self._raise_error(raise_cls)

    def _ensure_value_has_specific_length(
        self, length: int, raise_cls=NotHasSpecificLengthValueObjectError
    ):
        if len(self.value) != length:
            self._raise_error(raise_cls)
