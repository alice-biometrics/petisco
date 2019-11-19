from meiga import Result, Error

from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)

CLIENT_ID_LENGTH_LIMIT = 50


class ClientId(str):
    def __new__(cls, client_id):
        client_id = None if client_id == "None" else client_id
        return str.__new__(cls, client_id)

    def handle(self) -> Result[bool, Error]:
        if self is not None and len(self) > CLIENT_ID_LENGTH_LIMIT:
            return Result(failure=InputExceedLengthLimitError(message=self))
        else:
            return Result(success=True)
