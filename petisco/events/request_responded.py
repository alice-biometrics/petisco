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


class RequestResponded(Event):
    application: str
    controller: str
    is_success: bool
    status_code: int
    content: dict
    correlation_id: str
    elapsed_time: float
    additional_info: Dict[str, str]

    def __init__(
        self,
        application: str,
        controller: str,
        is_success: bool,
        http_response: Tuple[Dict, int],
        correlation_id: str,
        elapsed_time: float,
        additional_info: Dict[str, str],
    ):
        self.application = application
        self.controller = controller
        self.is_success = is_success
        self.correlation_id = correlation_id
        self.elapsed_time = elapsed_time
        self.additional_info = additional_info
        self.set_content_and_status_code(http_response)

        super().__init__()

    def set_content_and_status_code(self, http_response):
        content = REQUEST_RESPONDED_UNWRAP_ERROR
        status_code = 500
        if isinstance(http_response, Tuple):
            content = http_response[0]
            status_code = http_response[1]
        else:
            try:
                from flask import Response

                if isinstance(http_response, Response):
                    content = "binary"
                    status_code = http_response.status_code
            except (RuntimeError, ImportError):
                pass

        self.content = content
        self.status_code = status_code
