import json
import logging

import pytest
from meiga import Result

from petisco.controller.controller_decorator import controller
from petisco.controller.correlation_id import CorrelationId
from tests.unit.fake_logger import FakeLogger
from tests.unit.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_without_input_parameters():

    logger = FakeLogger()

    @controller(logger=logger)
    def my_controller():
        return Result("Hello Petisco")

    my_controller()

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        logging.INFO,
        LogMessageMother.get_controller(
            operation="my_controller", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        logging.INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            message="Result: Result[status: success | value: Hello Petisco]",
        ).to_json(),
    )

@pytest.mark.unit
def test_should_execute_successfully_a_empty_controller_with_correlation_id_as_only_input_parameter():

    logger = FakeLogger()

    @controller(logger=logger)
    def my_controller(correlation_id: CorrelationId):
        return Result("Hello Petisco")

    my_controller()

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    correlation_id = json.loads(first_logging_message[1])["correlation_id"]

    assert first_logging_message == (
        logging.INFO,
        LogMessageMother.get_controller(
            operation="my_controller", correlation_id=correlation_id, message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        logging.INFO,
        LogMessageMother.get_controller(
            operation="my_controller",
            correlation_id=correlation_id,
            message="Result: Result[status: success | value: Hello Petisco]",
        ).to_json(),
    )
