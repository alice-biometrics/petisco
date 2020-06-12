from petisco.domain.value_objects.string_value_object import StringValueObject
from petisco.domain.errors.given_input_is_not_valid_error import (
    GivenInputIsNotValidError,
)
from petisco.domain.errors.length_limit_string_value_object_error import (
    ExceedLengthLimitValueObjectError,
)


class ClientId(StringValueObject):
    def guard(self):
        self._ensure_is_less_than_50_chars()
        self._ensure_value_contains_valid_char(raise_cls=GivenInputIsNotValidError)

    def _ensure_is_less_than_50_chars(self):
        if len(self.value) > 50:
            raise ExceedLengthLimitValueObjectError(message=self.value)
