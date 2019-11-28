import re
from typing import Any

from meiga import Result, Error, Failure, Success

from petisco.domain.errors.given_input_is_not_valid_error import (
    GivenInputIsNotValidError,
)
from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)


class ClientId(str):
    def __new__(cls, client_id, length: int = 50):
        client_id = None if client_id == "None" else client_id
        cls.length = length
        return str.__new__(cls, client_id)

    def to_result(self) -> Result[Any, Error]:
        client_id = None if self == "None" else self

        if client_id is not None:
            if len(client_id) > self.length:
                return Failure(InputExceedLengthLimitError(message=client_id))
            else:
                if not re.search(
                    r"^[a-zA-Z]*(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", client_id
                ):
                    return Failure(GivenInputIsNotValidError(message=client_id))
        return Success(client_id)
