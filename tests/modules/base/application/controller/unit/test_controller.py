from __future__ import annotations

from datetime import datetime, timezone
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

from petisco import (
    Controller,
    CriticalError,
    DomainError,
    ErrorMap,
    HttpError,
    Middleware,
    NotFound,
    PrintMiddleware,
    UnknownError,
    custom_message_handler,
    unwrap_result_handler,
)
from petisco.base.application.application_info import ApplicationInfo


class MyError(Error):
    pass


def set_shared_error_map(shared_error_map: ErrorMap) -> None:
    ApplicationInfo(
        name="test_controller",
        organization="test",
        version="1",
        deployed_at=datetime.now(timezone.utc),
        force_recreation=True,
        shared_error_map=shared_error_map,
    )


def clear_shared_error_map() -> None:
    ApplicationInfo.clear()


@pytest.mark.unit
class TestController:
    def should_return_success_result(self):  # noqa
        class MyController(Controller):
            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()
        result.assert_success()

    def should_return_failure_result(self):  # noqa
        class MyController(Controller):
            def execute(self) -> BoolResult:
                return isFailure

        result = MyController().execute()
        result.assert_failure()

    def should_return_failure_result_with_critical_error_enriched_with_controller_parameters(  # noqa
        self,
    ):
        class MyCriticalError(CriticalError):
            pass

        class ControllerThatReturnEmptyCriticalError(Controller):
            def execute(self, param1: str, param2: int) -> Failure[MyCriticalError]:
                return Failure(MyCriticalError())

        class ControllerThatReturnEnrichedCriticalError(Controller):
            def execute(self, param1: str, param2: int) -> Failure[MyCriticalError]:
                return Failure(MyCriticalError(additional_info={"message": "error"}))

        result = ControllerThatReturnEmptyCriticalError().execute(
            param1="param1", param2=2
        )
        result.assert_failure(value_is_instance_of=MyCriticalError)
        assert result.value.additional_info.get("param1") == "param1"
        assert result.value.additional_info.get("param2") == "2"

        result = ControllerThatReturnEnrichedCriticalError().execute(
            param1="param1", param2=2
        )
        result.assert_failure(value_is_instance_of=MyCriticalError)
        assert result.value.additional_info.get("message") == "error"
        assert result.value.additional_info.get("param1") == "param1"
        assert result.value.additional_info.get("param2") == "2"

    def should_return_transformed_success_handler(self):  # noqa
        expected_result = {"message": "ok"}

        class MyController(Controller):
            class Config:
                success_handler = lambda result: expected_result  # noqa E731

            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()

        assert result.transform() == expected_result

    def should_return_transformed_by_error_map(self):  # noqa
        expected_result = {"message": "not ok"}

        class MyController(Controller):
            class Config:
                error_map = {MyError: expected_result}

            def execute(self) -> BoolResult:
                return Failure(MyError())

        result = MyController().execute()

        assert result.transform() == expected_result

    def should_return_transformed_by_default_error_map(self):  # noqa
        class MyController(Controller):
            def execute(self) -> BoolResult:
                return Failure(
                    NotFound()
                )  # NotFound is available in petisco.DEFAULT_HTTP_ERROR_MAP

        result = MyController().execute()

        assert result.transform() == HttpError(status_code=404)

    def should_return_transformed_by_shared_error_map(self):  # noqa
        expected_http_error = HttpError(status_code=425)

        class MySharedError(DomainError):
            ...

        set_shared_error_map({MySharedError: expected_http_error})

        class MyController(Controller):
            def execute(self) -> BoolResult:
                return Failure(
                    MySharedError()
                )  # MySharedError is defined in SHARED_ERROR_MAP

        result = MyController().execute()

        assert result.transform() == expected_http_error

        clear_shared_error_map()

    def should_return_transformed_with_priority_for_controller_error_map_instead_of_shared(
        self,
    ):  # noqa
        expected_http_error = HttpError(status_code=460)
        not_expected_http_error = HttpError(status_code=404)

        class MySharedAndConfiguredError(DomainError):
            ...

        set_shared_error_map({MySharedAndConfiguredError: not_expected_http_error})

        class MyController(Controller):
            class Config:
                error_map = {MySharedAndConfiguredError: expected_http_error}

            def execute(self) -> BoolResult:
                return Failure(MySharedAndConfiguredError())

        result = MyController().execute()

        assert result.transform() == expected_http_error
        assert result.transform() != not_expected_http_error

        clear_shared_error_map()

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
        result.assert_success()

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
        result.assert_success()

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

        result.assert_failure()
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

        result.assert_success()
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
        assert result.transform() == expected_result

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
        result.assert_failure(value_is_instance_of=UnknownError)

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

        assert result.transform() == expected_result

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

        assert result.transform() == expected_result

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
