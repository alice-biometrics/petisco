from __future__ import annotations

from unittest.mock import patch

import pytest
from meiga import BoolResult, Error, Failure, Success, isFailure, isSuccess

from petisco import AsyncController, PrintMiddleware, UnknownError


class MyError(Error):
    pass


@pytest.mark.unit
@pytest.mark.asyncio
class TestAsyncController:
    async def should_return_success_result(self):  # noqa
        class MyAsyncController(AsyncController):
            async def execute(self) -> BoolResult:
                return isSuccess

        result = await MyAsyncController().execute()
        result.assert_success()

    async def should_return_failure_result(self):  # noqa
        class MyAsyncController(AsyncController):
            async def execute(self) -> BoolResult:
                return isFailure

        result = await MyAsyncController().execute()
        result.assert_failure()

    async def should_return_mapped_success_handler(self):  # noqa
        expected_result = {"message": "ok"}

        class MyAsyncController(AsyncController):
            class Config:
                success_handler = lambda result: expected_result  # noqa E731

            async def execute(self) -> BoolResult:
                return isSuccess

        result = await MyAsyncController().execute()
        assert result.transform() == expected_result

    async def should_return_mapped_by_error_map(self):  # noqa
        expected_result = {"message": "not ok"}

        class MyAsyncController(AsyncController):
            class Config:
                error_map = {MyError: expected_result}

            async def execute(self) -> BoolResult:
                return Failure(MyError())

        result = await MyAsyncController().execute()

        assert result.transform() == expected_result

    @pytest.mark.parametrize(
        "configured_middlewares",
        [[], [PrintMiddleware], [PrintMiddleware, PrintMiddleware]],
    )
    async def should_return_success_result_with_middlewares(
        self,
        configured_middlewares,
    ):
        class MyAsyncController(AsyncController):
            class Config:
                middlewares = configured_middlewares

            async def execute(self) -> BoolResult:
                return isSuccess

        result = await MyAsyncController().execute()
        result.assert_success()

    @pytest.mark.parametrize(
        "configured_middlewares",
        ["", "PrintMiddleware", "PrintMiddleware,PrintMiddleware"],
    )
    async def should_return_success_result_with_middlewares_defined_by_envar(
        self, configured_middlewares, monkeypatch
    ):
        monkeypatch.setenv("PETISCO_DEFAULT_MIDDLEWARES", configured_middlewares)

        class MyAsyncController(AsyncController):
            async def execute(self) -> BoolResult:
                return isSuccess

        result = await MyAsyncController().execute()
        result.assert_success()

        monkeypatch.undo()

    @pytest.mark.parametrize("controller_result", [isSuccess, isFailure])
    async def should_execute_middleware_defined_in_controller(
        self,
        controller_result,
    ):
        class MyAsyncController(AsyncController):
            class Config:
                middlewares = [PrintMiddleware]

            async def execute(self) -> BoolResult:
                return controller_result

        with patch.object(
            PrintMiddleware, "before", return_value=isSuccess
        ) as mock_middleware_before:
            with patch.object(
                PrintMiddleware, "after", return_value=isSuccess
            ) as mock_middleware_after:
                result = await MyAsyncController().execute()

        assert result == controller_result
        mock_middleware_before.assert_called()
        mock_middleware_after.assert_called()

    async def should_execute_middleware_when_controller_raise_an_unexpected_exception(
        self,
    ):
        class MyAsyncController(AsyncController):
            class Config:
                middlewares = [PrintMiddleware]

            async def execute(self) -> BoolResult:
                raise Exception()

        with patch.object(
            PrintMiddleware, "before", return_value=isSuccess
        ) as mock_middleware_before:
            with patch.object(
                PrintMiddleware, "after", return_value=isSuccess
            ) as mock_middleware_after:
                result = await MyAsyncController().execute()

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
    async def should_raise_an_error_with_unavailable_middlewares_defined_by_envar(
        self, configured_middlewares, monkeypatch
    ):
        monkeypatch.setenv("PETISCO_DEFAULT_MIDDLEWARES", configured_middlewares)

        class MyAsyncController(AsyncController):
            async def execute(self) -> BoolResult:
                return isSuccess

        with pytest.raises(TypeError) as excinfo:
            await MyAsyncController().execute()

        assert " in PETISCO_DEFAULT_MIDDLEWARES is not valid. Please, use" in str(
            excinfo.value
        )

        monkeypatch.undo()

    async def should_execute_middleware_defined_by_envar(self, monkeypatch):
        monkeypatch.setenv("PETISCO_DEFAULT_MIDDLEWARES", "PrintMiddleware")

        class MyAsyncController(AsyncController):
            async def execute(self) -> BoolResult:
                return isSuccess

        with patch.object(
            PrintMiddleware, "before", return_value=isSuccess
        ) as mock_middleware_before:
            with patch.object(
                PrintMiddleware, "after", return_value=isSuccess
            ) as mock_middleware_after:
                result = await MyAsyncController().execute()

        result.assert_success()
        mock_middleware_before.assert_called()
        mock_middleware_after.assert_called()

        monkeypatch.undo()

    @pytest.mark.parametrize(
        "simulate_result, expected_result",
        [(isSuccess, {"message": "ok"}), (Failure(MyError()), {"message": "not ok"})],
    )
    async def should_works_with_all_configurations(
        self, simulate_result, expected_result
    ):
        class MyAsyncController(AsyncController):
            class Config:
                middlewares = [PrintMiddleware]
                success_handler = lambda result: expected_result  # noqa E731
                error_map = {MyError: expected_result}

            async def execute(self) -> BoolResult:
                return simulate_result

        result = await MyAsyncController().execute()
        assert result.transform() == expected_result

    async def should_raise_an_exception_if_execute_method_is_not_implemented(
        self,
    ):  # noqa
        with pytest.raises(NotImplementedError) as excinfo:

            class MyAsyncController(AsyncController):
                pass

            assert (
                excinfo.value.message
                == "Petisco Controller must implement an execute method"
            )

    async def should_return_unknown_error(self):  # noqa
        class MyAsyncController(AsyncController):
            async def execute(self, num: int) -> BoolResult:
                result = num / 0
                return Success(result)

        result = await MyAsyncController().execute(2)
        result.assert_failure(value_is_instance_of=UnknownError)
