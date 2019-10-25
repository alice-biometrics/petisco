import logging

import pytest

from petisco import UseCase, use_case_logger
from meiga import Result

from tests.unit.fake_logger import FakeLogger
from tests.unit.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_without_input_parameters_and_returning_a_string_result():

    logger = FakeLogger()

    @use_case_logger(logger=logger)
    class MyUseCase(UseCase):
        def execute(self):
            return Result("Hello Petisco")

    MyUseCase().execute()

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        logging.INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        logging.INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Result: Hello Petisco"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_with_input_parameters_but_not_in_the_whitelist():

    logger = FakeLogger()

    @use_case_logger(logger=logger)
    class MyUseCase(UseCase):
        def execute(self, client_id: str, user_id: str):
            return Result("Hello Petisco")

    MyUseCase().execute(client_id="client_id", user_id="user_id")

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        logging.INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        logging.INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Result: Hello Petisco"
        ).to_json(),
    )

@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_with_input_parameters():

    logger = FakeLogger()

    @use_case_logger(
        logger=logger, logging_parameters_whitelist=["client_id", "user_id"]
    )
    class MyUseCase(UseCase):
        def execute(self, client_id: str, user_id: str):
            return Result("Hello Petisco")

    MyUseCase().execute(client_id="client_id", user_id="user_id")

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]
    third_logging_message = logger.get_logging_messages()[2]

    assert first_logging_message == (
        logging.INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Start"
        ).to_json(),
    )
    assert second_logging_message == (
        logging.INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message={"client_id": "client_id", "user_id": "user_id"}
        ).to_json(),
    )
    assert third_logging_message == (
        logging.INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Result: Hello Petisco"
        ).to_json(),
    )
