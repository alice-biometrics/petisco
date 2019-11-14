from petisco.controller.errors.http_error import HttpError


class BadRequestHttpError(HttpError):
    def __init__(self, message: str = "Bad Request.", code: int = 400, suffix=""):
        if suffix:
            message = message + " " + suffix

        super(BadRequestHttpError, self).__init__(message, code)
