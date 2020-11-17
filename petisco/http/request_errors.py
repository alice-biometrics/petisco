import json
from json.decoder import JSONDecodeError

from meiga import Error


def get_error_message(error_message_title, response):
    error_message = {"error": error_message_title}

    try:
        detail = response.json()
        error_message["detal"] = detail
    except JSONDecodeError:
        pass

    return error_message


class RequestError(Error):
    def __init__(self, error_name: str, error_message: str, status_code: int):
        self.error_name = error_name
        self.error_message = error_message
        self.status_code = status_code


class MultipartFormatRequestError(RequestError):
    @staticmethod
    def from_response(response):
        error_message = get_error_message("Fail to create multipart", response)
        return MultipartFormatRequestError(
            error_name=str(__name__),
            error_message=json.dumps(error_message),
            status_code=response.status_code,
        )


class MissingSchemaRequestError(RequestError):
    def __init__(self):
        super().__init__(
            error_name=str(__name__),
            error_message=json.dumps({"error": "Missing schema in request"}),
            status_code=422,
        )


class TimeoutRequestError(RequestError):
    def __init__(self):
        super().__init__(
            error_name=str(__name__),
            error_message=json.dumps({"error": "Timeout error"}),
            status_code=408,
        )


class ConnectionRequestError(RequestError):
    def __init__(self):
        super().__init__(
            error_name=str(__name__),
            error_message=json.dumps({"error": "Connection error"}),
            status_code=503,
        )


class BadRequestError(RequestError):
    @staticmethod
    def from_response(response):
        error_message = get_error_message("Bad request Error", response)
        return BadRequestError(
            error_name=str(__name__),
            error_message=json.dumps(error_message),
            status_code=response.status_code,
        )


class UnauthorizedRequestError(RequestError):
    @staticmethod
    def from_response(response):
        error_message = get_error_message("Unauthorized error", response)
        return UnauthorizedRequestError(
            error_name=str(__name__),
            error_message=json.dumps(error_message),
            status_code=response.status_code,
        )


class UnknownRequestError(RequestError):
    @staticmethod
    def from_response(response):
        error_message = get_error_message("Unknown error", response)
        return UnknownRequestError(
            error_name=str(__name__),
            error_message=json.dumps(error_message),
            status_code=response.status_code,
        )
