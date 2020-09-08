from petisco.domain.value_objects.string_value_object import StringValueObject
from petisco.domain.errors.given_name_is_not_valid_error import GivenNameIsNotValidError


class Name(StringValueObject):
    def __init__(self, value: str):
        self.value = value
        super(Name, self).__init__(self.value)

    def guard(self):
        self._ensure_value_contains_valid_char(
            raise_cls=GivenNameIsNotValidError, allow_utf8mb4=False
        )
        self._ensure_value_is_less_than_n_char(50)
        self._ensure_value_is_greater_than_n_char(0)
