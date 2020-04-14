import base64
import os
from typing import Any

from meiga import Result, Failure, Error, Success

from petisco.domain.value_objects.value_object import ValueObject
from petisco.domain.errors.exceed_length_limit_value_error_error import (
    ExceedLengthLimitValueObjectError,
)

LENGTH = 16


class UserId(str, ValueObject):
    def __new__(cls, user_id, length=LENGTH):
        user_id = None if user_id == "None" else user_id
        cls.length = length
        return str.__new__(cls, user_id)

    def to_result(self) -> Result[Any, Error]:
        user_id = None if self == "None" else self

        if user_id is not None and len(user_id) > self.length:
            return Failure(ExceedLengthLimitValueObjectError(message=user_id))
        else:
            return Success(user_id)

    @staticmethod
    def generate():
        r = os.urandom(LENGTH)
        return UserId(base64.b64encode(r, altchars=b"-_").decode("utf-8")[:LENGTH])
