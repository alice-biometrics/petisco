import pytest
from meiga import Success, isFailure

from petisco import controller_handler, ERROR, INFO, __version__
from petisco.events.request_responded import RequestResponded
from petisco.events.event_config import EventConfig
from tests.unit.mocks.fake_event_manager import FakeEventManager
from tests.unit.mocks.fake_logger import FakeLogger
from tests.unit.mocks.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_without_input_parameters(
    given_any_info_id, given_headers_provider
):

    logger = FakeLogger()
    event_manager = FakeEventManager()
    event_topic = "controller"

    @controller_handler(
        app_name="petisco",
        app_version=__version__,
        logger=logger,
        event_config=EventConfig(event_manager=event_manager, event_topic=event_topic),
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller(headers=None):
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start", info_id=given_any_info_id
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
            info_id=given_any_info_id,
        ).to_json(),
    )

    request_responded = event_manager.get_sent_events(event_topic)[0]
    assert isinstance(request_responded, RequestResponded)
    assert request_responded.app_name == "petisco"
    assert request_responded.app_version == __version__
    assert request_responded.controller == "my_controller"
    assert request_responded.is_success is True
    assert request_responded.http_response["content"] == '{"message": "OK"}'
    assert request_responded.http_response["status_code"] == 200
    assert request_responded.additional_info is None


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_client_id_and_user_id_inputs(
    given_any_info_id, given_headers_provider
):

    fake_logger = FakeLogger()
    fake_event_manager = FakeEventManager()
    event_topic = "controller"
    event_additional_info = ["client_id", "user_id"]

    @controller_handler(
        logger=fake_logger,
        event_config=EventConfig(
            event_manager=fake_event_manager,
            event_topic=event_topic,
            event_additional_info=event_additional_info,
        ),
        headers_provider=given_headers_provider(given_any_info_id.get_http_headers()),
    )
    def my_controller(client_id, user_id, headers=None):
        return Success("Hello Petisco")

    http_response = my_controller(client_id="client-id", user_id="user-id")

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = fake_logger.get_logging_messages()[0]
    second_logging_message = fake_logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start", info_id=given_any_info_id
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
            info_id=given_any_info_id,
        ).to_json(),
    )

    request_responded = fake_event_manager.get_sent_events(event_topic)[0]
    assert isinstance(request_responded, RequestResponded)
    assert request_responded.app_name == "app-undefined"
    assert request_responded.app_version is None
    assert request_responded.controller == "my_controller"
    assert request_responded.is_success is True
    assert request_responded.http_response["content"] == '{"message": "OK"}'
    assert request_responded.http_response["status_code"] == 200
    assert request_responded.additional_info == {
        "client_id": "client-id",
        "user_id": "user-id",
    }


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_correlation_id_as_only_input_parameter(
    given_any_info_id, given_headers_provider
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
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start", info_id=given_any_info_id
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
            info_id=given_any_info_id,
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_with_a_failure_a_empty_controller_without_input_parameters(
    given_any_info_id, given_headers_provider
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
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start", info_id=given_any_info_id
        ).to_json(),
    )

    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: failure | value: Error]",
            info_id=given_any_info_id,
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_with_a_failure_a_empty_controller_with_correlation_id_as_only_input_parameter(
    given_any_info_id, given_headers_provider
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
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start", info_id=given_any_info_id
        ).to_json(),
    )
    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: failure | value: Error]",
            info_id=given_any_info_id,
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_without_input_parameters_and_logger():
    @controller_handler()
    def my_controller(headers=None):
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)


@pytest.mark.unit
def test_should_execute_successfully_a_filtered_object_by_blacklist(
    given_any_info_id, given_headers_provider
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
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start", info_id=given_any_info_id
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Success result of type: bytes",
            info_id=given_any_info_id,
        ).to_json(),
    )


@pytest.mark.unit
def test_should_log_an_exception_occurred_on_the_controller(
    given_any_info_id, given_headers_provider
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
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start", info_id=given_any_info_id
        ).to_json(),
    )

    assert second_logging_message[0] == ERROR
    assert "line" in second_logging_message[1]
    assert "RuntimeError" in second_logging_message[1]
    assert "my_controller exception" in second_logging_message[1]
