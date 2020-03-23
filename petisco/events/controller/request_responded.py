from typing import Tuple, Dict

from petisco.events.event import Event


class RequestResponded(Event):
    is_success: bool
    controller: str
    service: str
    correlation_id: str
    elapsed_time: float
    status_code: int
    content: dict

    def __init__(
        self,
        is_success: bool,
        http_response: Tuple[Dict, int],
        controller: str,
        service: str,
        correlation_id: str,
        elapsed_time: float,
    ):
        self.is_success = is_success
        self.controller = controller
        self.service = service
        self.correlation_id = correlation_id
        self.elapsed_time = elapsed_time
        self.content = http_response[0]
        self.status_code = http_response[1]
        super().__init__()
