import json

import pytest
from meiga import Success, isFailure

from petisco import controller_handler, CorrelationId, ERROR, INFO
from tests.unit.mocks.fake_logger import FakeLogger
from tests.unit.mocks.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_without_input_parameters():

    logger = FakeLogger()

    @controller_handler(logger=logger)
    def my_controller(headers):
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result[status: success | value: Hello Petisco]",
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_correlation_id_as_only_input_parameter():

    logger = FakeLogger()

    @controller_handler(logger=logger)
    def my_controller(headers, correlation_id: CorrelationId):
        return Success("Hello Petisco")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    correlation_id = json.loads(first_logging_message[1])["correlation_id"]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", correlation_id=correlation_id, message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            correlation_id=correlation_id,
            message="Result[status: success | value: Hello Petisco]",
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_with_a_failure_a_empty_controller_without_input_parameters():

    logger = FakeLogger()

    @controller_handler(logger=logger)
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
            operation="my_controller", message="Start"
        ).to_json(),
    )

    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller", message="Result[status: failure | value: Error]"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_execute_with_a_failure_a_empty_controller_with_correlation_id_as_only_input_parameter():

    logger = FakeLogger()

    @controller_handler(logger=logger)
    def my_controller(correlation_id: CorrelationId, headers=None):
        return isFailure

    http_response = my_controller()

    assert http_response == (
        {"error": {"message": "Unknown Error", "type": "HttpError"}},
        500,
    )

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    correlation_id = json.loads(first_logging_message[1])["correlation_id"]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", correlation_id=correlation_id, message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_controller(
            operation="my_controller",
            correlation_id=correlation_id,
            message="Result[status: failure | value: Error]",
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
def test_should_execute_successfully_a_filtered_object_by_blacklist():

    logger = FakeLogger()

    @controller_handler(logger=logger)
    def my_controller(headers=None):
        return Success(b"This are bytes")

    http_response = my_controller()

    assert http_response == ({"message": "OK"}, 200)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Success result of type: bytes"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_log_an_exception_occurred_on_the_controller():

    logger = FakeLogger()

    @controller_handler(logger=logger)
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
            operation="my_controller", message="Start"
        ).to_json(),
    )

    assert second_logging_message[0] == ERROR
    assert "line" in second_logging_message[1]
    assert "RuntimeError" in second_logging_message[1]
    assert "my_controller exception" in second_logging_message[1]
