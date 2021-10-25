from typing import NamedTuple

import pytest
from meiga.assertions import assert_failure, assert_success

from petisco import UseCase, use_case_handler, ERROR, DEBUG, UnknownError
from meiga import Success, Failure, isFailure, isSuccess, Error

from tests.modules.unit.mocks.fake_logger import FakeLogger
from tests.modules.unit.mocks.log_message_mother import LogMessageMother


@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_without_input_parameters_and_returning_a_string_result(
    given_any_petisco,
):

    logger = FakeLogger()

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self):
            return Success("Hello Petisco")

    MyUseCase().execute()

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Hello Petisco"
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_with_input_parameters_but_not_in_the_whitelist(
    given_any_petisco,
):

    logger = FakeLogger()

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self, client_id: str, user_id: str):
            return Success("Hello Petisco")

    MyUseCase().execute(client_id="client_id", user_id="user_id")

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Hello Petisco"
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_with_input_parameters(
    given_any_petisco,
):

    logger = FakeLogger()

    @use_case_handler(
        logger=logger, logging_parameters_whitelist=["client_id", "user_id"]
    )
    class MyUseCase(UseCase):
        def execute(self, client_id: str, user_id: str):
            return Success("Hello Petisco")

    result = MyUseCase().execute(client_id="client_id", user_id="user_id")

    assert_success(result)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]
    third_logging_message = logger.get_logging_messages()[2]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase",
            message={"client_id": "client_id", "user_id": "user_id"},
        ).to_dict(),
    )
    assert third_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Hello Petisco"
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_filtered_object_by_blacklist_with_python_type_bytes(
    given_any_petisco,
):

    logger = FakeLogger()

    @use_case_handler(logger=logger, logging_types_blacklist=[bytes])
    class MyUseCase(UseCase):
        def execute(self):
            return Success(b"This are bytes")

    result = MyUseCase().execute()

    assert_success(result)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Success result of type: bytes"
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_filtered_object_by_blacklist_with_own_named_tuple(
    given_any_petisco,
):

    logger = FakeLogger()

    class BinaryInfo(NamedTuple):
        name: str
        data: bytes

    @use_case_handler(logger=logger, logging_types_blacklist=[BinaryInfo])
    class MyUseCase(UseCase):
        def execute(self):
            binary_info = BinaryInfo(name="my_data", data=b"This are bytes")
            return Success(binary_info)

    result = MyUseCase().execute()

    assert_success(result)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Success result of type: BinaryInfo"
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_filtered_object_by_blacklist_with_a_tuple(
    given_any_petisco,
):

    logger = FakeLogger()

    @use_case_handler(logger=logger, logging_types_blacklist=[tuple])
    class MyUseCase(UseCase):
        def execute(self):
            binary_info = ("my_data", b"This are bytes")
            return Success(binary_info)

    result = MyUseCase().execute()

    assert_success(result)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Success result of type: tuple"
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_log_successfully_a_large_type_with_its_repr(given_any_petisco):

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

    result = MyUseCase().execute()

    assert_success(result)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert second_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="<BinaryInfo my_data, len(data)=14>"
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_log_successfully_an_error_returned_on_a_use_case(given_any_petisco):

    logger = FakeLogger()

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self):
            return isFailure

    result = MyUseCase().execute()

    assert_failure(result, value_is_instance_of=Error)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Result[status: failure | value: Error] "
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_log_successfully_an_error_raised_by_a_meiga_handler(given_any_petisco):

    logger = FakeLogger()

    class UserNotFoundError(Error):
        pass

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self):
            Failure(UserNotFoundError()).unwrap_or_return()
            return isSuccess

    result = MyUseCase().execute()

    assert_failure(result, value_is_instance_of=UserNotFoundError)

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert second_logging_message == (
        ERROR,
        LogMessageMother.get_use_case(
            operation="MyUseCase",
            message="Result[status: failure | value: UserNotFoundError] ",
        ).to_dict(),
    )


@pytest.mark.unit
def test_should_use_case_handler_return_a_failure_with_unknown_error_when_raise_an_uncontrolled_exception(
    given_any_petisco,
):

    logger = FakeLogger()
    expected_raised_exception = RuntimeError("uncontrolled exception")

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self):
            raise expected_raised_exception

    result = MyUseCase().execute()

    assert_failure(
        result,
        value_is_instance_of=UnknownError,
        value_is_equal_to=UnknownError(expected_raised_exception),
    )

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert (
        "value: UnknownError (MyUseCase (Use Case)): RuntimeError: uncontrolled exception.\nTraceback (most recent call last):\n  File"
        in second_logging_message[1]["data"]["message"]
    )


@pytest.mark.unit
def test_should_use_case_handler_return_a_failure_with_unknown_error_when_raise_an_uncontrolled_exception_with_input_parameters(
    given_any_petisco,
):

    logger = FakeLogger()
    expected_raised_exception = RuntimeError("uncontrolled exception")
    input_text = "my-text"
    input_verbose = True

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self, text: str, verbose: bool):
            raise expected_raised_exception

    result = MyUseCase().execute(text=input_text, verbose=input_verbose)

    assert_failure(
        result,
        value_is_instance_of=UnknownError,
        value_is_equal_to=UnknownError(expected_raised_exception),
    )

    assert {"text": "my-text", "verbose": True} == result.value.input_parameters

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert (
        "value: UnknownError (MyUseCase (Use Case)): RuntimeError: uncontrolled exception.\nTraceback (most recent call last):\n  File"
        in second_logging_message[1]["data"]["message"]
    )


@pytest.mark.unit
def test_should_use_case_handler_return_a_failure_with_unknown_error_when_raise_an_uncontrolled_exception_with_non_defined_input_parameters(
    given_any_petisco,
):

    logger = FakeLogger()
    expected_raised_exception = RuntimeError("uncontrolled exception")
    input_text = "my-text"
    input_verbose = True

    @use_case_handler(logger=logger)
    class MyUseCase(UseCase):
        def execute(self, text: str, verbose: bool):
            raise expected_raised_exception

    result = MyUseCase().execute(input_text, input_verbose)

    assert_failure(
        result,
        value_is_instance_of=UnknownError,
        value_is_equal_to=UnknownError(expected_raised_exception),
    )

    assert {"param_1": "my-text", "param_2": True} == result.value.input_parameters

    first_logging_message = logger.get_logging_messages()[0]
    second_logging_message = logger.get_logging_messages()[1]

    assert first_logging_message == (
        DEBUG,
        LogMessageMother.get_use_case(
            operation="MyUseCase", message="Running Use Case"
        ).to_dict(),
    )
    assert (
        "value: UnknownError (MyUseCase (Use Case)): RuntimeError: uncontrolled exception.\nTraceback (most recent call last):\n  File"
        in second_logging_message[1]["data"]["message"]
    )


@pytest.mark.unit
def test_should_log_successfully_a_non_error_use_case_with_default_parameters(
    given_any_petisco,
):
    @use_case_handler()
    class MyUseCase(UseCase):
        def execute(self):
            return Success("Hello Petisco")

    MyUseCase().execute()
