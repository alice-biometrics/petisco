from unittest.mock import Mock

import pytest
from meiga import Success, isFailure, Failure

from petisco import controller_handler, ERROR, __version__, DEBUG, IEventBus
from petisco.domain.errors.critical_error import CriticalError
from petisco.event.shared.domain.request_responded import RequestResponded
from tests.modules.unit.mocks.fake_logger import FakeLogger
from tests.modules.unit.mocks.fake_notifier import FakeNotifier
from tests.modules.unit.mocks.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_without_input_parameters(
    given_any_petisco, given_any_info_id, given_headers_provider
):

    logger = FakeLogger()
    mock_event_bus = Mock(IEventBus)

    @controller_handler(
        app_name="petisco",
        app_version=__version__,
        logger=logger,
        send_request_responded_event=True,
        event_bus=mock_event_bus,
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller():
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Processing Request",
            info_id=given_any_info_id,
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
            info_id=given_any_info_id,
        ).to_dict(),
    )

    request_responded = mock_event_bus.publish.call_args[0][0]
    assert isinstance(request_responded, RequestResponded)
    assert request_responded.app_name == "petisco"
    assert request_responded.app_version == __version__
    assert request_responded.controller == "my_controller"
    assert request_responded.is_success is True
    assert request_responded.http_response["content"] == {
        "message": '{"message": "OK"}',
        "message_size": 17,
    }
    assert request_responded.http_response["status_code"] == 200


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_correlation_id_as_only_input_parameter(
    given_any_petisco, given_any_info_id, given_headers_provider
):

    logger = FakeLogger()

    @controller_handler(
        logger=logger,
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller(headers=None):
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Processing Request",
            info_id=given_any_info_id,
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
            info_id=given_any_info_id,
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_execute_with_a_failure_a_empty_controller_without_input_parameters(
    given_any_petisco, given_any_info_id, given_headers_provider
):

    logger = FakeLogger()

    @controller_handler(
        logger=logger,
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller(headers=None):
        return isFailure

    http_response = my_controller()

    assert http_response == (
        {"error": {"message": "Unknown Error", "type": "HttpError"}},
        500,
    )

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Processing Request",
            info_id=given_any_info_id,
        ).to_dict(),
    )

    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: failure | value: Error]",
            info_id=given_any_info_id,
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_execute_with_a_failure_a_empty_controller_with_correlation_id_as_only_input_parameter(
    given_any_petisco, given_any_info_id, given_headers_provider
):

    logger = FakeLogger()

    @controller_handler(
        logger=logger,
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller(headers=None):
        return isFailure

    http_response = my_controller()

    assert http_response == (
        {"error": {"message": "Unknown Error", "type": "HttpError"}},
        500,
    )

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Processing Request",
            info_id=given_any_info_id,
        ).to_dict(),
    )
    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: failure | value: Error]",
            info_id=given_any_info_id,
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_default_parameters(
    given_any_petisco
):
    @controller_handler()
    def my_controller(headers=None):
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)


@pytest.mark.unit
def test_should_execute_successfully_a_filtered_object_by_blacklist(
    given_any_petisco, given_any_info_id, given_headers_provider
):

    logger = FakeLogger()

    @controller_handler(
        logger=logger,
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller(headers=None):
        return Success(b"This are bytes")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Processing Request",
            info_id=given_any_info_id,
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Success result of type: bytes",
            info_id=given_any_info_id,
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_log_an_exception_occurred_on_the_controller(
    given_any_petisco, given_any_info_id, given_headers_provider
):

    logger = FakeLogger()

    @controller_handler(
        logger=logger,
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller(headers=None):
        raise RuntimeError("my_controller exception")

    http_response = my_controller()

    assert http_response == (
        {"error": {"message": "Internal Error.", "type": "InternalHttpError"}},
        500,
    )

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Processing Request",
            info_id=given_any_info_id,
        ).to_dict(),
    )

    assert second_logging_message[0] == ERROR
    assert "line" in second_logging_message[1]["data"]["message"]
    assert "RuntimeError" in second_logging_message[1]["data"]["message"]
    assert "my_controller exception" in second_logging_message[1]["data"]["message"]


@pytest.mark.unit
def test_should_notify_an_exception_occurred_on_the_controller(
    given_any_petisco, given_any_info_id, given_headers_provider
):

    notifier = FakeNotifier()

    @controller_handler(
        notifier=notifier,
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller(headers=None):
        raise RuntimeError("my_controller exception")

    http_response = my_controller()

    assert http_response == (
        {"error": {"message": "Internal Error.", "type": "InternalHttpError"}},
        500,
    )

    assert notifier.publish_called
    assert notifier.publish_times_called == 1


@pytest.mark.unit
def test_should_notify_a_critical_error_on_the_controller(
    given_any_petisco, given_any_info_id, given_headers_provider
):

    notifier = FakeNotifier()

    class MyCriticalError(CriticalError):
        pass

    @controller_handler(
        notifier=notifier,
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller(headers=None):
        return Failure(MyCriticalError())

    http_response = my_controller()

    assert http_response == (
        {"error": {"message": "Internal Error.", "type": "InternalHttpError"}},
        500,
    )

    assert notifier.publish_called
    assert notifier.publish_times_called == 1
