from petisco.controller.errors.http_error import HttpError


class InternalHttpError(HttpError):
    def __init__(self, message: str = "Internal Error.", code: int = 500, suffix=""):
        if suffix:
            message = message + " " + suffix

        super(InternalHttpError, self).__init__(message, code)
