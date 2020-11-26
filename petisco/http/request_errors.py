import json
from json.decoder import JSONDecodeError

from meiga import Error

from petisco.domain.timedelta_parser import TimeDeltaParser


def get_error_message(error_message_title, response):
    error_message = {"error": error_message_title}

    try:
        detail = response.json()
        error_message["detail"] = detail
    except JSONDecodeError:
        pass

    return error_message


class RequestError(Error):
    def __init__(
        self,
        error_name: str,
        error_message: str,
        status_code: int,
        headers: dict = None,
        content: dict = None,
        completed_in_ms: float = None,
    ):
        self.error_name = error_name
        self.error_message = error_message
        self.status_code = status_code
        self.headers = headers if headers else None
        self._set_content(content)
        self.completed_in_ms = completed_in_ms

    def _set_content(self, content):
        self.content = None
        if content:
            try:
                if isinstance(content, bytes):
                    content = content.decode()
                self.content = json.loads(content)
            except Exception:
                pass

    def __repr__(self):
        return f"{self.error_name} ({self.status_code}) -> {self.error_message} (completed_in: {self.completed_in_ms})"


class MultipartFormatRequestError(RequestError):
    @staticmethod
    def from_response(response):
        error_message = get_error_message("Fail to create multipart", response)
        return MultipartFormatRequestError(
            error_name="MultipartFormatRequestError",
            error_message=json.dumps(error_message),
            status_code=response.status_code,
            headers=response.headers,
            content=response.content,
            completed_in_ms=TimeDeltaParser.ms_from_timedelta(response.elapsed),
        )


class MissingSchemaRequestError(RequestError):
    def __init__(self):
        super().__init__(
            error_name="MissingSchemaRequestError",
            error_message=json.dumps({"error": "Missing schema in request"}),
            status_code=422,
        )


class TimeoutRequestError(RequestError):
    def __init__(self):
        super().__init__(
            error_name="TimeoutRequestError",
            error_message=json.dumps({"error": "Timeout error"}),
            status_code=408,
        )


class ConnectionRequestError(RequestError):
    def __init__(self):
        super().__init__(
            error_name="ConnectionRequestError",
            error_message=json.dumps({"error": "Connection error"}),
            status_code=503,
        )


class BadRequestError(RequestError):
    @staticmethod
    def from_response(response):
        error_message = get_error_message("Bad request Error", response)
        return BadRequestError(
            error_name="BadRequestError",
            error_message=json.dumps(error_message),
            status_code=response.status_code,
            headers=response.headers,
            content=response.content if response.content else response.text,
            completed_in_ms=TimeDeltaParser.ms_from_timedelta(response.elapsed),
        )


class UnauthorizedRequestError(RequestError):
    @staticmethod
    def from_response(response):
        error_message = get_error_message("Unauthorized error", response)
        return UnauthorizedRequestError(
            error_name="UnauthorizedRequestError",
            error_message=json.dumps(error_message),
            status_code=response.status_code,
            headers=response.headers,
            content=response.content,
            completed_in_ms=TimeDeltaParser.ms_from_timedelta(response.elapsed),
        )


class UnknownRequestError(RequestError):
    @staticmethod
    def from_response(response):
        error_message = get_error_message("Unknown error", response)
        return UnknownRequestError(
            error_name="UnknownRequestError",
            error_message=json.dumps(error_message),
            status_code=response.status_code,
            headers=response.headers,
            content=response.content,
            completed_in_ms=TimeDeltaParser.ms_from_timedelta(response.elapsed),
        )

    @staticmethod
    def from_exception(exc):
        return UnknownRequestError(
            error_name="UnknownRequestError", error_message=str(exc), status_code=500
        )
