import base64
import os
from typing import Any

from meiga import Result, Failure, Error, Success

from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)

LENGTH = 12


class UserId(str):
    def __new__(cls, user_id, length=LENGTH):
        user_id = None if user_id == "None" else user_id
        cls.length = length
        return str.__new__(cls, user_id)

    def to_result(self) -> Result[Any, Error]:
        user_id = None if self == "None" else self

        if user_id is not None and len(user_id) > self.length:
            return Failure(InputExceedLengthLimitError(message=user_id))
        else:
            return Success(user_id)

    @staticmethod
    def generate():
        r = os.urandom(LENGTH)
        return UserId(base64.b64encode(r, altchars=b"-_").decode("utf-8")[:LENGTH])
