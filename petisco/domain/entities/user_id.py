import base64
import os

from meiga import Result, Failure

from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)

LENGTH = 12


class UserId(str):
    def __new__(cls, user_id, length=LENGTH):
        user_id = None if user_id == "None" else user_id
        cls.length = length
        return str.__new__(cls, user_id)

    def handle(self) -> Result:
        if self is not None and len(self) > self.length:
            return Failure(InputExceedLengthLimitError(message=self))
        else:
            return self

    @staticmethod
    def generate():
        r = os.urandom(LENGTH)
        return UserId(base64.b64encode(r, altchars=b"-_").decode("utf-8")[:LENGTH])
