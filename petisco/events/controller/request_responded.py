from meiga import Result

from petisco.events.event import Event


class RequestResponded(Event):
    is_success: bool
    controller: str
    service: str
    correlation_id: str
    elapsed_time: float

    def __init__(
        self,
        result: Result,
        controller: str,
        service: str,
        correlation_id: str,
        elapsed_time: float,
    ):
        self.is_success = result.is_success
        self.controller = controller
        self.service = service
        self.correlation_id = correlation_id
        self.elapsed_time = elapsed_time
        super().__init__()
