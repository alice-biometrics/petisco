from typing import Any
from unittest import mock
from unittest.mock import Mock

import pytest
from meiga import Failure, Success, isSuccess

from petisco import (
    AlreadyExists,
    Builder,
    Controller,
    CriticalError,
    Dependency,
    DomainEventBus,
    HttpError,
    NotImplementedDomainEventBus,
)
from petisco.base.application.application_info import ApplicationInfo
from petisco.base.application.dependency_injection.container import Container
from petisco.base.application.middleware.request_responded_middleware import (
    RequestRespondedMiddleware,
)

LONG_MESSAGE_TO_ENFORCE_TRIMMING = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
LONG_SUCCESS_RESPONSE = "Response OK (Trimmed message: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the )"
LONG_FAILURE_RESPONSE = "Response Error (Trimmed message: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the )"


class MyCriticalError(CriticalError):
    pass


@pytest.mark.unit
class TestRequestRespondedMiddleware:
    request_responded_middleware: RequestRespondedMiddleware

    def setup_method(self) -> None:
        ApplicationInfo(name="app_name", version="app_version")
        event_bus_dependency = Dependency(
            DomainEventBus, builders={"default": Builder(NotImplementedDomainEventBus)}
        )
        Container.set_dependencies([event_bus_dependency], overwrite=True)

        self.request_responded_middleware = RequestRespondedMiddleware()
        self.request_responded_middleware.set_data(
            wrapped_class_name="class_name", wrapped_class_input_arguments=()
        )

    def teardown_method(self) -> None:
        Container.clear()
        ApplicationInfo.clear()

    @mock.patch("petisco.NotImplementedDomainEventBus.publish")
    @pytest.mark.parametrize(
        "controller_result, controller_message, status_code",
        [
            (isSuccess, True, 200),
            (Success("Successful response"), "Successful response", 200),
            (Success(LONG_MESSAGE_TO_ENFORCE_TRIMMING), LONG_SUCCESS_RESPONSE, 200),
        ],
    )
    def should_publish_event_with_success_response(
        self,
        mock_event_bus: Mock,
        controller_result: Any,
        controller_message: Any,
        status_code: int,
    ) -> None:
        class MyController(Controller):
            class Config:
                middlewares = [RequestRespondedMiddleware]

            def execute(self, info_id: str) -> Any:
                return controller_result

        mock_event_bus.return_value = isSuccess

        result = MyController().execute(info_id="info_id")
        result.assert_success()

        mock_event_bus.assert_called_once()
        domain_event_args = mock_event_bus.call_args.args[0]
        domain_event_attributes = domain_event_args.get_message_attributes()
        assert domain_event_attributes["controller"] == "MyController"
        assert domain_event_attributes["is_success"] is True
        assert (
            domain_event_attributes["http_response"]["content"]["message"]
            == controller_message
        )
        assert domain_event_attributes["http_response"]["status_code"] == status_code
        assert domain_event_attributes["info_id"] == "info_id"

    @mock.patch("petisco.NotImplementedDomainEventBus.publish")
    @pytest.mark.parametrize(
        "controller_result, controller_message, status_code",
        [
            (Failure(AlreadyExists()), "Already Exists", 404),
            (Failure(MyCriticalError()), "MyCriticalError", 500),
            (Failure(LONG_MESSAGE_TO_ENFORCE_TRIMMING), LONG_FAILURE_RESPONSE, 500),
        ],
    )
    def should_publish_event_with_failure_response(
        self,
        mock_event_bus: Mock,
        controller_result: Any,
        controller_message: Any,
        status_code: int,
    ) -> None:
        class MyController(Controller):
            class Config:
                middlewares = [RequestRespondedMiddleware]
                error_map = {
                    AlreadyExists: HttpError(
                        status_code=404, detail=controller_message
                    ),
                }

            def execute(self, info_id: str) -> Any:
                return controller_result

        result = MyController().execute(info_id="info_id")
        result.assert_failure()

        mock_event_bus.assert_called_once()
        domain_event_args = mock_event_bus.call_args.args[0]
        domain_event_attributes = domain_event_args.get_message_attributes()
        assert domain_event_attributes["controller"] == "MyController"
        assert domain_event_attributes["is_success"] is False
        assert (
            domain_event_attributes["http_response"]["content"]["message"]
            == controller_message
        )
        assert domain_event_attributes["http_response"]["status_code"] == status_code
        assert domain_event_attributes["info_id"] == "info_id"
