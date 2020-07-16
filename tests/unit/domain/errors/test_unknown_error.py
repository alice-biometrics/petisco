import traceback

import pytest
from meiga.assertions import assert_failure
from meiga.decorators import meiga

from petisco.domain.errors.unknown_error import UnknownError


@pytest.mark.unit
def test_should_construct_unknown_error_from_base_exception():

    error = UnknownError(Exception("my_trace"))

    assert error.message == "Exception: my_trace"


@pytest.mark.unit
def test_should_construct_unknown_error_from_runtime_error_exception():

    error = UnknownError(RuntimeError("my_trace"))

    assert error.message == "RuntimeError: my_trace"


@pytest.mark.unit
def test_should_capture_an_exception_during_runtime():

    expected_raised_exception = RuntimeError("my_trace")

    def inner():
        raise expected_raised_exception

    @meiga
    def method():
        try:
            inner()
        except Exception as exception:
            raise UnknownError(exception)

    result = method()

    assert_failure(
        result,
        value_is_instance_of=UnknownError,
        value_is_equal_to=UnknownError(expected_raised_exception),
    )


@pytest.mark.unit
def test_should_capture_an_exception_with_additional_context():

    expected_trace = "my_trace"
    expected_raised_exception = RuntimeError(expected_trace)

    def inner():
        raise expected_raised_exception

    @meiga
    def method():
        try:
            inner()
        except Exception as exception:
            raise UnknownError(
                exception=exception,
                executor="executor",
                traceback=traceback.format_exc(),
            )

    result = method()
    assert_failure(
        result,
        value_is_instance_of=UnknownError,
        value_is_equal_to=UnknownError(expected_raised_exception),
    )

    assert result.value.executor == "executor"
    assert "Traceback" in result.value.traceback
    assert "File" in result.value.traceback

    assert "Traceback" in str(result)
