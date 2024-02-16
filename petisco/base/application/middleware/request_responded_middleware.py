import time
from typing import Any

from loguru import logger
from meiga import AnyResult

from petisco import DomainEventBus
from petisco.base.application.application_info import ApplicationInfo
from petisco.base.application.dependency_injection.container import Container
from petisco.base.application.middleware.middleware import Middleware
from petisco.base.application.middleware.request_responded import RequestResponded


class RequestRespondedMiddleware(Middleware):
    """
    Middleware Implementation to generate events with information on request responses.
    """

    start_time: float

    def __init__(self) -> None:
        self.event_bus = Container.get(DomainEventBus)

    def get_info_id_from_input(self) -> Any:
        try:
            return self.wrapped_class_input_arguments.get("info_id", None)
        except Exception as exc:
            logger.error(
                f"Middleware error getting info_id on get_meta_from_input: {str(exc)}"
            )
        return None

    def before(self) -> None:
        self.start_time = time.time()

    def after(self, result: AnyResult) -> None:
        application_info = ApplicationInfo()

        elapsed_time = time.time() - self.start_time
        info_id = self.get_info_id_from_input()

        result_transform = result.transform()

        request_responded = RequestResponded.create(
            app_name=application_info.name,
            app_version=application_info.version,
            controller=f"{self.wrapped_class_name}",
            is_success=result.is_success,
            http_response=result_transform,
            elapsed_time=elapsed_time,
            info_id=info_id,
        )
        self.event_bus.publish(request_responded)
