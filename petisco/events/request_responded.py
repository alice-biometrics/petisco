import inspect
import json
import traceback
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


def is_flask_response(value):
    try:
        from flask import Response

        if isinstance(value, Response):
            return True
    except (RuntimeError, ImportError):
        pass
    return False


def is_success(status_code: int):
    return 200 >= status_code <= 299


def get_content(response, status_code):
    if is_flask_response(response):
        return {"message": "flask response"}
    else:
        content = response
        if isinstance(content, str):
            content = json.loads(content)
        content_size = len(str(content))

        if content_size > 300:
            if is_success(status_code):
                content = {
                    "message": "Response OK (Trimmed message: message too long)",
                    "message_size": content_size,
                }
            else:
                error_type = content.get("error", {}).get("type", "Error")

                content = {
                    "error": {
                        "type": error_type,
                        "message": "Response Error (Trimmed message: message too long)",
                        "message_size": content_size,
                    }
                }

        return content


class RequestResponded(Event):
    app_name: str
    app_version: str
    controller: str
    is_success: bool
    http_response: Dict
    elapsed_time: float
    event_version: str = None

    def __init__(
        self,
        app_name: str,
        app_version: str,
        controller: str,
        is_success: bool,
        http_response: Tuple[Dict, int],
        elapsed_time: float,
    ):
        self.app_name = app_name
        self.app_version = app_version
        self.controller = controller
        self.is_success = is_success
        self.elapsed_time = elapsed_time
        self.set_http_response(http_response)
        super().__init__()

    def set_http_response(self, http_response):
        try:
            _http_response = {
                "content": REQUEST_RESPONDED_UNWRAP_ERROR,
                "status_code": 500,
            }
            if isinstance(http_response, Tuple):
                _http_response["content"] = get_content(
                    http_response[0], http_response[1]
                )
                _http_response["status_code"] = http_response[1]
            else:
                _http_response["content"] = get_content(
                    http_response, http_response.status_code
                )
                _http_response["status_code"] = http_response.status_code
        except Exception as e:  # noqa E722
            traceback.print_exc()
            frame_info = inspect.stack()[1]
            raise ImportError(
                f"Error parsing response on Petisco RequestResponded Event\n"
                f"\tfilename: {frame_info.filename}\n"
                f"\tlineno: {frame_info.lineno}\n"
                f"\tfunction: {frame_info.function}\n"
                f"\tcode_context: {frame_info.code_context}"
            )
        self.http_response = _http_response
