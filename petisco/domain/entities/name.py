from meiga import Result, Error

from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)

NAME_LENGTH_LIMIT = 50


class Name(str):
    def __new__(cls, name):
        name = None if name == "None" else name
        return str.__new__(cls, name)

    def handle(self) -> Result[bool, Error]:
        if self is not None and len(self) > NAME_LENGTH_LIMIT:
            return Result(failure=InputExceedLengthLimitError(message=self))
        else:
            return Result(success=True)
