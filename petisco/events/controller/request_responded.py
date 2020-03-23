from typing import Tuple, Dict

from petisco.events.event import Event


class RequestResponded(Event):
    application: str
    controller: str
    is_success: bool
    status_code: int
    content: dict
    correlation_id: str
    elapsed_time: float

    def __init__(
        self,
        application: str,
        controller: str,
        is_success: bool,
        http_response: Tuple[Dict, int],
        correlation_id: str,
        elapsed_time: float,
    ):
        self.application = application
        self.controller = controller
        self.is_success = is_success
        self.content = http_response[0]
        self.status_code = http_response[1]
        self.correlation_id = correlation_id
        self.elapsed_time = elapsed_time

        super().__init__()
