from petisco.controller.errors.http_error import HttpError


class InvalidTokenHttpError(HttpError):
    def __init__(
        self,
        message: str = "Access token is missing or invalid.",
        code: int = 401,
        suffix="",
    ):
        if suffix:
            message = message + " " + suffix

        super(InvalidTokenHttpError, self).__init__(message, code)
