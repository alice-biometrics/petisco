import pytest
from meiga import AnyResult, BoolResult, Error, Failure, Result, Success, isSuccess

from petisco import AsyncAppService, AsyncUseCase, UseCaseUncontrolledError
from petisco.extra.meiga import WaitingForEarlyReturn


class MyError(Error):
    pass


@pytest.mark.unit
@pytest.mark.asyncio
class TestAsyncUseCase:
    async def should_return_success_result(self):
        class MyUseCase(AsyncUseCase):
            async def execute(self, param_1: int, param_2: int) -> Result[int, Error]:
                return Success(param_1 + param_2)

        result = await MyUseCase().execute(2, 3)

        result.assert_success(value_is_instance_of=int, value_is_equal_to=5)

    async def should_return_failure_result(self):
        class MyUseCase(AsyncUseCase):
            async def execute(self) -> BoolResult:
                return Failure(MyError())

        result = await MyUseCase().execute()

        result.assert_failure(value_is_instance_of=MyError)

    async def should_return_failure_result_when_raise_on_failure_exception_from_meiga(
        self,
    ):
        class MyUseCase(AsyncUseCase):
            async def execute(self) -> BoolResult:
                raise WaitingForEarlyReturn(Failure(MyError()))

        result = await MyUseCase().execute()

        result.assert_failure(value_is_instance_of=MyError)

    async def should_return_failure_result_when_raise_an_uncontrolled_error_with_executor_and_traceback(
        self,
    ):
        expected_exception = TypeError("whatever")

        class MyUseCase(AsyncUseCase):
            async def execute(self) -> BoolResult:
                raise expected_exception

        result = await MyUseCase().execute()

        result.assert_failure(
            value_is_instance_of=UseCaseUncontrolledError,
            value_is_equal_to=UseCaseUncontrolledError(expected_exception),
        )
        assert __name__ in result.value.traceback
        assert "whatever" in result.value.traceback
        assert MyUseCase.__name__ == result.value.executor

    async def should_return_failure_result_when_raise_an_uncontrolled_error_with_input_parameters(
        self,
    ):
        expected_exception = TypeError("whatever")

        class MyUseCase(AsyncUseCase):
            async def execute(self, param1: str, param2: str) -> BoolResult:
                raise expected_exception

        result = await MyUseCase().execute("param1_value", param2="param2_value")

        result.assert_failure(
            value_is_instance_of=UseCaseUncontrolledError,
            value_is_equal_to=UseCaseUncontrolledError(expected_exception),
        )
        assert result.value.input_parameters["param1"] == "param1_value"
        assert result.value.input_parameters["param2"] == "param2_value"

    async def should_only_wrap_with_meiga_checker_execute_method(self):
        class MyUseCase(AsyncUseCase):
            async def execute(self) -> BoolResult:
                return isSuccess

            async def other_method(self):
                raise TypeError("whatever")

        result = await MyUseCase().execute()
        result.assert_success()

        with pytest.raises(TypeError):
            await MyUseCase().other_method()

    async def should_raise_an_exception_if_execute_method_is_not_implemented(self):
        with pytest.raises(NotImplementedError) as excinfo:

            class MyUseCase(AsyncUseCase):
                pass

            assert (
                excinfo.value.message
                == "Petisco AsyncUseCase must implement an execute method"
            )

    async def should_success_when_using_collaborators(self):
        class MyAppService(AsyncAppService):
            async def execute(self) -> AnyResult:
                return isSuccess

        class MyUseCase(AsyncUseCase):
            def __init__(
                self, app_service_1: MyAppService, app_service_2: MyAppService
            ):
                self.app_service_1 = app_service_1
                self.app_service_2 = app_service_2

            async def execute(self) -> BoolResult:
                (await self.app_service_1.execute()).unwrap_or_return()
                (await self.app_service_2.execute()).unwrap_or_return()
                return isSuccess

        result = await MyUseCase(
            app_service_1=MyAppService(), app_service_2=MyAppService()
        ).execute()

        result.assert_success()
