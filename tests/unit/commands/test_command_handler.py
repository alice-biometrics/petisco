import pytest
from meiga import Success
from meiga.assertions import assert_success, assert_failure

from petisco import INFO, command_handler, Event
from tests.unit.mocks.fake_logger import FakeLogger
from tests.unit.mocks.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_execute_successfully_a_empty_command_without_input_parameters(
    given_any_correlation_id
):

    logger = FakeLogger()

    @command_handler(logger=logger)
    def my_command(event: Event):
        return Success("Hello Petisco")

    event = Event({"event_correlation_id": given_any_correlation_id})
    result = my_command(event=event)

    assert_success(result)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]
    assert first_logging_message == (
        INFO,
        LogMessageMother.get_command(
            operation="my_command",
            message=f"Event received: {event}",
            correlation_id=given_any_correlation_id,
        ).to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_command(
            operation="my_command",
            message="Result[status: success | value: Hello Petisco]",
            correlation_id=given_any_correlation_id,
        ).to_json(),
    )


@pytest.mark.unit
def test_should_raise_a_type_error_when_a_command_do_not_receive_a_event():

    logger = FakeLogger()

    @command_handler(logger=logger)
    def my_command():
        return Success("Hello Petisco")

    with pytest.raises(TypeError):
        my_command()


@pytest.mark.unit
def test_should_raise_a_type_error_when_a_command_do_not_receive_a_event_but_from_other_type():

    logger = FakeLogger()

    @command_handler(logger=logger)
    def my_command(event: str):
        return Success("Hello Petisco")

    with pytest.raises(TypeError):
        my_command()


@pytest.mark.unit
def test_should_return_failure_result_when_an_exception_raises_within_command(
    given_any_correlation_id
):

    logger = FakeLogger()

    @command_handler(logger=logger)
    def my_command(event: Event):
        raise RuntimeError("my_command exception")

    event = Event({"event_correlation_id": given_any_correlation_id})
    result = my_command(event=event)

    assert_failure(result)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]
    assert first_logging_message == (
        INFO,
        LogMessageMother.get_command(
            operation="my_command",
            message=f"Event received: {event}",
            correlation_id=given_any_correlation_id,
        ).to_json(),
    )
    assert "line" in second_logging_message[1]
    assert "RuntimeError" in second_logging_message[1]
    assert "my_command exception" in second_logging_message[1]
