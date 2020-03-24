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

REQUEST_RESPONDED_VERSION = "1.2.0"


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
    application: str
    controller: str
    is_success: bool
    http_response: Dict
    correlation_id: str
    elapsed_time: float
    additional_info: Dict[str, str]
    version: str = None

    def __init__(
        self,
        application: str,
        controller: str,
        is_success: bool,
        http_response: Tuple[Dict, int],
        correlation_id: str,
        elapsed_time: float,
        additional_info: Dict[str, str],
        version: str = REQUEST_RESPONDED_VERSION,
    ):
        self.application = application
        self.controller = controller
        self.is_success = is_success
        self.correlation_id = correlation_id
        self.elapsed_time = elapsed_time
        self.additional_info = additional_info
        self.set_http_response(http_response)
        self.version = version
        super().__init__()

    def set_http_response(self, http_response):
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

        self.http_response = _http_response
