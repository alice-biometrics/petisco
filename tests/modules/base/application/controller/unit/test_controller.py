from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest
from meiga import (
    AnyResult,
    BoolResult,
    Error,
    Failure,
    Result,
    Success,
    isFailure,
    isSuccess,
)
from meiga.assertions import assert_failure, assert_success

from petisco import (
    Controller,
    ControllerResult,
    Middleware,
    PrintMiddleware,
    UnknownError,
    custom_message_handler,
    unwrap_result_handler,
)


class MyError(Error):
    pass


@pytest.mark.unit
class TestController:
    def should_return_success_result(self):  # noqa
        class MyController(Controller):
            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()
        assert_success(result)

    def should_return_failure_result(self):  # noqa
        class MyController(Controller):
            def execute(self) -> BoolResult:
                return isFailure

        result = MyController().execute()
        assert_failure(result)

    def should_return_mapped_success_handler(self):  # noqa
        expected_result = {"message": "ok"}

        class MyController(Controller):
            class Config:
                success_handler = lambda result: expected_result  # noqa E731

            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()

        assert result == expected_result

    def should_return_mapped_by_error_map(self):  # noqa
        expected_result = {"message": "not ok"}

        class MyController(Controller):
            class Config:
                error_map = {MyError: expected_result}

            def execute(self) -> BoolResult:
                return Failure(MyError())

        result = MyController().execute()

        assert result == expected_result

    @pytest.mark.parametrize(
        "configured_middlewares",
        [[], [PrintMiddleware], [PrintMiddleware, PrintMiddleware]],
    )
    def should_return_success_result_with_middlewares(
        self,
        configured_middlewares,
    ):
        class MyController(Controller):
            class Config:
                middlewares = configured_middlewares

            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()
        assert_success(result)

    @pytest.mark.parametrize(
        "configured_middlewares",
        ["", "PrintMiddleware", "PrintMiddleware,PrintMiddleware"],
    )
    def should_return_success_result_with_middlewares_defined_by_envar(
        self, configured_middlewares, monkeypatch
    ):
        monkeypatch.setenv("PETISCO_DEFAULT_MIDDLEWARES", configured_middlewares)

        class MyController(Controller):
            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()
        assert_success(result)

        monkeypatch.undo()

    @pytest.mark.parametrize("controller_result", [isSuccess, isFailure])
    def should_execute_middleware_defined_in_controller(
        self,
        controller_result,
    ):
        class MyController(Controller):
            class Config:
                middlewares = [PrintMiddleware]

            def execute(self) -> BoolResult:
                return controller_result

        with patch.object(
            PrintMiddleware, "before", return_value=isSuccess
        ) as mock_middleware_before:
            with patch.object(
                PrintMiddleware, "after", return_value=isSuccess
            ) as mock_middleware_after:
                result = MyController().execute()

        assert result == controller_result
        mock_middleware_before.assert_called()
        mock_middleware_after.assert_called()

    def should_execute_middleware_when_controller_raise_an_unexpected_exception(self):
        class MyController(Controller):
            class Config:
                middlewares = [PrintMiddleware]

            def execute(self) -> BoolResult:
                raise Exception()

        with patch.object(
            PrintMiddleware, "before", return_value=isSuccess
        ) as mock_middleware_before:
            with patch.object(
                PrintMiddleware, "after", return_value=isSuccess
            ) as mock_middleware_after:
                result = MyController().execute()

        assert result.is_failure
        mock_middleware_before.assert_called()
        mock_middleware_after.assert_called()

    @pytest.mark.parametrize(
        "configured_middlewares",
        [
            "NotAvailable",
            "NotAvailable,PrintMiddleware",
            "NotAvailable,NotAvailable",
            ",",
            ",,",
            "None",
        ],
    )
    def should_raise_an_error_with_unavailable_middlewares_defined_by_envar(
        self, configured_middlewares, monkeypatch
    ):
        monkeypatch.setenv("PETISCO_DEFAULT_MIDDLEWARES", configured_middlewares)

        class MyController(Controller):
            def execute(self) -> BoolResult:
                return isSuccess

        with pytest.raises(TypeError) as excinfo:
            MyController().execute()

        assert " in PETISCO_DEFAULT_MIDDLEWARES is not valid. Please, use" in str(
            excinfo.value
        )

        monkeypatch.undo()

    def should_execute_middleware_defined_by_envar(self, monkeypatch):
        monkeypatch.setenv("PETISCO_DEFAULT_MIDDLEWARES", "PrintMiddleware")

        class MyController(Controller):
            def execute(self) -> BoolResult:
                return isSuccess

        with patch.object(
            PrintMiddleware, "before", return_value=isSuccess
        ) as mock_middleware_before:
            with patch.object(
                PrintMiddleware, "after", return_value=isSuccess
            ) as mock_middleware_after:
                result = MyController().execute()

        assert result.is_success
        mock_middleware_before.assert_called()
        mock_middleware_after.assert_called()

        monkeypatch.undo()

    @pytest.mark.parametrize(
        "simulate_result, expected_result",
        [(isSuccess, {"message": "ok"}), (Failure(MyError()), {"message": "not ok"})],
    )
    def should_works_with_all_configurations(self, simulate_result, expected_result):
        class MyController(Controller):
            class Config:
                middlewares = [PrintMiddleware]
                success_handler = lambda result: expected_result  # noqa E731
                error_map = {MyError: expected_result}

            def execute(self) -> BoolResult:
                return simulate_result

        result = MyController().execute()
        assert result == expected_result

    def should_raise_an_exception_if_execute_method_is_not_implemented(self):  # noqa
        with pytest.raises(NotImplementedError) as excinfo:

            class MyController(Controller):
                pass

            assert (
                excinfo.value.message
                == "Petisco Controller must implement an execute method"
            )

    def should_return_unknown_error(self):  # noqa
        class MyController(Controller):
            def execute(self, num: int) -> BoolResult:
                result = num / 0
                return Success(result)

        result = MyController().execute(2)

        assert_failure(result, value_is_instance_of=UnknownError)

    def should_succees_when_return_typed_controller_result(self):  # noqa
        class MyController(Controller[int]):
            def execute(self) -> ControllerResult:
                return Success(1)

        def function() -> int:
            return MyController().execute()

        function()

    def should_fail_when_return_type_is_not_a_result(self):  # noqa
        class MyController(Controller[int]):
            def execute(self) -> ControllerResult:
                return 1

        with pytest.raises(TypeError, match="Controller Error"):
            MyController().execute()

    def should_skip_mapping_when_return_type_is_not_a_result(self):  # noqa
        class MyController(Controller[int]):
            class Config:
                skip_result_mapping = True

            def execute(self) -> ControllerResult:
                return 1

        result = MyController().execute()

        assert isinstance(result, int)

    def should_return_result_value_from_success_handler_with_unwrap_result_handler(
        self,
    ):  # noqa
        expected_result = {"message": "ok"}

        class MyController(Controller):
            class Config:
                success_handler = unwrap_result_handler

            def execute(self) -> Result[dict[str, Any], Error]:
                return Success(expected_result)

        result = MyController().execute()

        assert result == expected_result

    def should_return_result_value_from_success_handler_with_custom_message_handler(
        self,
    ):  # noqa
        expected_result = {"message": "my-custom-message"}

        class MyController(Controller):
            class Config:
                success_handler = custom_message_handler(expected_result)

            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()

        assert result == expected_result

    def should_not_fail_when_middleware_raise_unexpected_error_on_before(self):  # noqa
        class RaiseErrorOnBeforeMiddleware(Middleware):
            def before(self) -> None:
                raise RuntimeError("Error in before")

            def after(self, result: AnyResult) -> None:
                pass

        class MyController(Controller):
            class Config:
                middlewares = [RaiseErrorOnBeforeMiddleware]

            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()

        result.assert_success()

    def should_not_fail_when_middleware_raise_unexpected_error_on_after(self):  # noqa
        class RaiseErrorOnAfterMiddleware(Middleware):
            def before(self) -> None:
                pass

            def after(self, result: AnyResult) -> None:
                raise RuntimeError("Error in after")

        class MyController(Controller):
            class Config:
                middlewares = [RaiseErrorOnAfterMiddleware]

            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()

        result.assert_success()
