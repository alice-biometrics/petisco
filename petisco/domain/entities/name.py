import re
from meiga import Result, Error, Failure

from petisco.domain.errors.given_input_is_not_valid_error import (
    GivenInputIsNotValidError,
)
from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)

NAME_LENGTH_LIMIT = 50


class Name(str):
    def __new__(cls, name, length_limit: int = 50):
        name = None if name == "None" else name
        cls.length_limit = length_limit
        return str.__new__(cls, name)

    def handle(self) -> Result[bool, Error]:
        if self is not None:
            if len(self) > self.length_limit:
                return Failure(InputExceedLengthLimitError(message=self))
            else:
                if not re.search(r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", self):
                    return Failure(GivenInputIsNotValidError(message=self))
        return self
