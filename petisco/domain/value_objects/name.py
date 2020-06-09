from petisco.domain.value_objects.string_value_object import StringValueObject
from petisco.domain.errors.given_name_is_not_valid_error import GivenNameIsNotValidError
from petisco.domain.errors.exceed_length_limit_value_error_error import (
    ExceedLengthLimitValueObjectError,
)


class Name(StringValueObject):
    def __init__(self, value: str):
        self.value = value
        super(Name, self).__init__(self.value)

    def guard(self):
        self._ensure_value_is_less_than_50_chars()
        self._ensure_value_contains_valid_char(raise_cls=GivenNameIsNotValidError)

    def _ensure_value_is_less_than_50_chars(self):
        if len(self.value) > 50:
            raise ExceedLengthLimitValueObjectError(message=self.value)
