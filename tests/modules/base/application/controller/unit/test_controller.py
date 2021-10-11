import pytest
from meiga import BoolResult, Error, Failure, Success, isFailure, isSuccess
from meiga.assertions import assert_failure, assert_success

from petisco import Controller, PrintMiddleware, UnknownError


class MyError(Error):
    pass


@pytest.mark.unit
def test_controller_should_return_success_result():
    class MyController(Controller):
        def execute(self) -> BoolResult:
            return isSuccess

    result = MyController().execute()
    assert_success(result)


@pytest.mark.unit
def test_controller_should_return_failure_result():
    class MyController(Controller):
        def execute(self) -> BoolResult:
            return isFailure

    result = MyController().execute()
    assert_failure(result)


@pytest.mark.unit
def test_controller_should_return_mapped_success_handler():
    expected_result = {"message", "ok"}

    class MyController(Controller):
        class Config:
            success_handler = lambda result: expected_result  # noqa E731

        def execute(self) -> BoolResult:
            return isSuccess

    result = MyController().execute()

    assert result == expected_result


@pytest.mark.unit
def test_controller_should_return_mapped_by_error_map():
    expected_result = {"message", "not ok"}

    class MyController(Controller):
        class Config:
            error_map = {MyError: expected_result}

        def execute(self) -> BoolResult:
            return Failure(MyError())

    result = MyController().execute()

    assert result == expected_result


@pytest.mark.unit
@pytest.mark.parametrize(
    "configured_middlewares",
    [[], [PrintMiddleware], [PrintMiddleware, PrintMiddleware]],
)
def test_controller_should_return_success_result_with_middlewares(
    configured_middlewares,
):
    class MyController(Controller):
        class Config:
            middlewares = configured_middlewares

        def execute(self) -> BoolResult:
            return isSuccess

    result = MyController().execute()
    assert_success(result)


@pytest.mark.unit
@pytest.mark.parametrize(
    "simulate_result, expected_result",
    [(isSuccess, {"message", "ok"}), (Failure(MyError()), {"message", "not ok"})],
)
def test_controller_should_works_with_all_configurations(
    simulate_result, expected_result
):
    class MyController(Controller):
        class Config:
            middlewares = [PrintMiddleware]
            success_handler = lambda result: expected_result  # noqa E731
            error_map = {MyError: expected_result}

        def execute(self) -> BoolResult:
            return simulate_result

    result = MyController().execute()
    assert result == expected_result


@pytest.mark.unit
def test_controller_should_raise_an_exception_if_execute_method_is_not_implemented():

    with pytest.raises(NotImplementedError) as excinfo:

        class MyController(Controller):
            pass

        assert (
            excinfo.value.message
            == "Petisco Controller must implement an execute method"
        )


@pytest.mark.unit
def test_controller_should_return_unknown_error():
    class MyController(Controller):
        def execute(self, num: int) -> BoolResult:
            result = num / 0
            return Success(result)

    result = MyController().execute(2)

    assert_failure(result, value_is_instance_of=UnknownError)