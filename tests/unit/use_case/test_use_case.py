from typing import NamedTuple

import pytest

from petisco import UseCase, use_case_handler, INFO
from meiga import Result, Success

from tests.unit.mocks.fake_logger import FakeLogger
from tests.unit.mocks.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_without_input_parameters_and_returning_a_string_result():

    logger = FakeLogger()

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self):
            return Result("Hello Petisco")

    MyUseCase().execute()

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_use_case(operation="MyUseCase", message="Start").to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Hello Petisco"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_with_input_parameters_but_not_in_the_whitelist():

    logger = FakeLogger()

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self, client_id: str, user_id: str):
            return Result("Hello Petisco")

    MyUseCase().execute(client_id="client_id", user_id="user_id")

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_use_case(operation="MyUseCase", message="Start").to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Hello Petisco"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_with_input_parameters():

    logger = FakeLogger()

    @use_case_handler(
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
        INFO,
        LogMessageMother.get_use_case(operation="MyUseCase", message="Start").to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase",
            message={"client_id": "client_id", "user_id": "user_id"},
        ).to_json(),
    )
    assert third_logging_message == (
        INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Hello Petisco"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_filtered_object_by_blacklist_with_python_type_bytest():

    logger = FakeLogger()

    @use_case_handler(logger=logger, logging_types_blacklist=[bytes])
    class MyUseCase(UseCase):
        def execute(self):
            return Success(b"This are bytes")

    MyUseCase().execute()

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_use_case(operation="MyUseCase", message="Start").to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Object of type: bytes"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_filtered_object_by_blacklist_with_own_named_tuple():

    logger = FakeLogger()

    class BinaryInfo(NamedTuple):
        name: str
        data: bytes

    @use_case_handler(logger=logger, logging_types_blacklist=[BinaryInfo])
    class MyUseCase(UseCase):
        def execute(self):
            binary_info = BinaryInfo(name="my_data", data=b"This are bytes")
            return Success(binary_info)

    MyUseCase().execute()

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_use_case(operation="MyUseCase", message="Start").to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Object of type: BinaryInfo"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_filtered_object_by_blacklist_with_a_tuple():

    logger = FakeLogger()

    @use_case_handler(logger=logger, logging_types_blacklist=[tuple])
    class MyUseCase(UseCase):
        def execute(self):
            binary_info = ("my_data", b"This are bytes")
            return Success(binary_info)

    MyUseCase().execute()

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_use_case(operation="MyUseCase", message="Start").to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Object of type: tuple"
        ).to_json(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_large_type_with_its_repr():

    logger = FakeLogger()

    class BinaryInfo(NamedTuple):
        name: str
        data: bytes

        def __repr__(self) -> str:
            return f"<BinaryInfo {self.name}, len(data)={len(self.data)}>"

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self):
            binary_info = BinaryInfo(name="my_data", data=b"This are bytes")
            return Success(binary_info)

    MyUseCase().execute()

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        INFO,
        LogMessageMother.get_use_case(operation="MyUseCase", message="Start").to_json(),
    )
    assert second_logging_message == (
        INFO,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="<BinaryInfo my_data, len(data)=14>"
        ).to_json(),
    )