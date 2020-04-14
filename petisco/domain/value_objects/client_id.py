import re
from typing import Any

from meiga import Result, Error, Failure, Success

from petisco.domain.value_objects.value_object import ValueObject
from petisco.domain.errors.given_input_is_not_valid_error import (
    GivenInputIsNotValidError,
)
from petisco.domain.errors.exceed_length_limit_value_error_error import (
    ExceedLengthLimitValueObjectError,
)


class ClientId(str, ValueObject):
    def __new__(cls, client_id, max_length: int = 50):
        client_id = None if client_id == "None" else client_id
        cls.max_length = max_length
        return str.__new__(cls, client_id)

    def to_result(self) -> Result[Any, Error]:
        client_id = None if self == "None" else self

        if client_id is not None:
            if len(client_id) > self.max_length:
                return Failure(ExceedLengthLimitValueObjectError(message=client_id))
            else:
                if not re.search(
                    r"^[a-zA-Z]*(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", client_id
                ):
                    return Failure(GivenInputIsNotValidError(message=client_id))
        return Success(client_id)
