import inspect
import json
from typing import Tuple, Dict

from petisco.events.event import Event

REQUEST_RESPONDED_UNWRAP_ERROR = (
    {
        "error": {
            "type": "RequestRespondedUnwrapError",
            "message": "Cannot unwrap http response from decorated function",
        }
    },
)

REQUEST_RESPONDED_VERSION = "1.4.0"


def is_flask_response(value):
    try:
        from flask import Response

        if isinstance(value, Response):
            return True
    except (RuntimeError, ImportError):
        pass
    return False


def get_content(value):
    if is_flask_response(value):
        return "flask response"
    else:
        return json.dumps(value)


class RequestResponded(Event):
    app_name: str
    app_version: str
    controller: str
    is_success: bool
    http_response: Dict
    elapsed_time: float
    additional_info: Dict[str, str]
    event_version: str = None

    def __init__(
        self,
        app_name: str,
        app_version: str,
        controller: str,
        is_success: bool,
        http_response: Tuple[Dict, int],
        elapsed_time: float,
        additional_info: Dict[str, str],
        event_version: str = REQUEST_RESPONDED_VERSION,
    ):
        self.app_name = app_name
        self.app_version = app_version
        self.controller = controller
        self.is_success = is_success
        self.elapsed_time = elapsed_time
        self.additional_info = additional_info
        self.set_http_response(http_response)
        self.event_version = event_version
        super().__init__()

    def set_http_response(self, http_response):
        try:
            _http_response = {
                "content": json.dumps(REQUEST_RESPONDED_UNWRAP_ERROR),
                "status_code": 500,
            }
            if isinstance(http_response, Tuple):
                _http_response["content"] = get_content(http_response[0])
                _http_response["status_code"] = http_response[1]
            else:
                _http_response["content"] = get_content(http_response)
                _http_response["status_code"] = http_response.status_code
        except Exception as e:  # noqa E722
            frame_info = inspect.stack()[1]
            raise ImportError(
                f"Error parsing response on Petisco RequestResponded Event\n"
                f"\tfilename: {frame_info.filename}\n"
                f"\tlineno: {frame_info.lineno}\n"
                f"\tfunction: {frame_info.function}\n"
                f"\tcode_context: {frame_info.code_context}"
            )
        self.http_response = _http_response
