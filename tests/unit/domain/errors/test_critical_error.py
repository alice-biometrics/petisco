import traceback

import pytest
from meiga.assertions import assert_failure
from meiga.decorators import meiga

from petisco.domain.errors.critical_error import CriticalError


@pytest.mark.unit
def test_should_construct_critical_error_from_base_exception():

    error = CriticalError(Exception("my_trace"))

    assert error.message == "Exception: my_trace"


@pytest.mark.unit
def test_should_construct_critical_error_from_runtime_error_exception():

    error = CriticalError(RuntimeError("my_trace"))

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
            raise CriticalError(exception)

    result = method()

    assert_failure(
        result,
        value_is_instance_of=CriticalError,
        value_is_equal_to=CriticalError(expected_raised_exception),
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
            raise CriticalError(
                exception=exception,
                executor="executor",
                traceback=traceback.format_exc(),
            )

    result = method()
    assert_failure(
        result,
        value_is_instance_of=CriticalError,
        value_is_equal_to=CriticalError(expected_raised_exception),
    )

    assert result.value.executor == "executor"
    assert "Traceback" in result.value.traceback
    assert "File" in result.value.traceback

    assert "Traceback" in str(result)


@pytest.mark.unit
def test_should_construct_critical_error_from_base_exception_and_valid_input_parameters():
    valid_input_parameters = ("hola", 2)

    error = CriticalError(
        Exception("my_trace"), input_parameters=valid_input_parameters
    )

    assert error.message == "Exception: my_trace"
    assert "Input Parameters: {'param_1': 'hola', 'param_2': 2}" in error.__repr__()


@pytest.mark.unit
def test_should_construct_critical_error_from_base_exception_and_valid_input_parameters_filtering_parameters():
    valid_input_parameters = ("hola", 2)

    error = CriticalError(
        Exception("my_trace"),
        input_parameters=valid_input_parameters,
        filter_parameters=["param_2"],
    )

    assert error.message == "Exception: my_trace"
    assert "Input Parameters: {'param_1': 'hola'}" in error.__repr__()
