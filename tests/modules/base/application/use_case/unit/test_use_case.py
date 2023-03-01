import pytest
from meiga import BoolResult, Error, Failure, Result, Success, isSuccess
from meiga.assertions import assert_failure, assert_success
from meiga.on_failure_exception import OnFailureException

from petisco import UseCase, UseCaseUncontrolledError


class MyError(Error):
    pass


@pytest.mark.unit
def test_use_case_should_return_success_result():
    class MyUseCase(UseCase):
        def execute(self, param_1: int, param_2: int) -> Result[int, Error]:
            return Success(param_1 + param_2)

    result = MyUseCase().execute(2, 3)

    assert_success(result, value_is_instance_of=int, value_is_equal_to=5)


@pytest.mark.unit
def test_use_case_should_return_failure_result():
    class MyUseCase(UseCase):
        def execute(self) -> BoolResult:
            return Failure(MyError())

    result = MyUseCase().execute()

    assert_failure(result, value_is_instance_of=MyError)


@pytest.mark.unit
def test_use_case_should_return_failure_result_when_raise_on_failure_exception_from_meiga():
    class MyUseCase(UseCase):
        def execute(self) -> BoolResult:
            raise OnFailureException(Failure(MyError()))

    result = MyUseCase().execute()

    assert_failure(result, value_is_instance_of=MyError)


@pytest.mark.unit
def test_use_case_should_return_failure_result_when_raise_an_uncontrolled_error_with_executor_and_traceback():

    expected_exception = TypeError("whatever")

    class MyUseCase(UseCase):
        def execute(self) -> BoolResult:
            raise expected_exception

    result = MyUseCase().execute()

    assert_failure(
        result,
        value_is_instance_of=UseCaseUncontrolledError,
        value_is_equal_to=UseCaseUncontrolledError(expected_exception),
    )
    assert __name__ in result.value.traceback
    assert "whatever" in result.value.traceback
    assert MyUseCase.__name__ == result.value.executor


@pytest.mark.unit
def test_use_case_should_return_failure_result_when_raise_an_uncontrolled_error_with_input_parameters():
    expected_exception = TypeError("whatever")

    class MyUseCase(UseCase):
        def execute(self, param1: str, param2: str) -> BoolResult:
            raise expected_exception

    result = MyUseCase().execute("param1_value", param2="param2_value")

    assert_failure(
        result,
        value_is_instance_of=UseCaseUncontrolledError,
        value_is_equal_to=UseCaseUncontrolledError(expected_exception),
    )
    assert result.value.input_parameters["param1"] == "param1_value"
    assert result.value.input_parameters["param2"] == "param2_value"


@pytest.mark.unit
def test_use_case_should_only_wrap_with_meiga_checker_execute_method():
    class MyUseCase(UseCase):
        def execute(self) -> BoolResult:
            return isSuccess

        def other_method(self):
            raise TypeError("whatever")

    result = MyUseCase().execute()
    assert_success(result)

    with pytest.raises(TypeError):
        MyUseCase().other_method()


@pytest.mark.unit
def test_use_case_should_raise_an_exception_if_execute_method_is_not_implemented():

    with pytest.raises(NotImplementedError) as excinfo:

        class MyUseCase(UseCase):
            pass

        assert (
            excinfo.value.message == "Petisco UseCase must implement an execute method"
        )
