from aifc import Error
from typing import Any, Dict
from unittest.mock import patch

import elasticapm
import pytest
from fastapi import HTTPException
from loguru import logger
from meiga import AnyResult, BoolResult, Failure, Result, Success, isFailure, isSuccess

from petisco import AlreadyExists, DomainError, HttpError, NotFound, PrintMiddleware
from petisco.extra.fastapi import (
    FASTAPI_DEFAULT_RESPONSE,
    FastAPIController,
    as_fastapi,
    assert_http_exception,
)


@pytest.mark.unit
class TestFastApiController:
    def should_return_dict_when_success_result(self):
        class MyController(FastAPIController):
            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()
        assert as_fastapi(result) == FASTAPI_DEFAULT_RESPONSE

    def should_raise_http_exception_when_failure_result(self):
        class MyController(FastAPIController):
            def execute(self) -> BoolResult:
                return isFailure

        with pytest.raises(HTTPException) as excinfo:
            result = MyController().execute()
            as_fastapi(result)

        assert excinfo.value.status_code == 500
        assert excinfo.value.detail == "Unknown Error"

    @patch.object(logger, "error")
    @patch.object(elasticapm, "set_custom_context")
    def should_logging_error_with_traceback_and_inject_in_apm(
        self, apm_set_custom_context_mock, logger_error_mock
    ):
        class MyController(FastAPIController):
            def execute(self) -> BoolResult:
                raise TypeError("test_error")

        with pytest.raises(HTTPException):
            result = MyController().execute()
            as_fastapi(result)

        apm_set_custom_context_mock.assert_called()
        apm_internal_error_message = apm_set_custom_context_mock.call_args[0][0][
            "internal_error_message"
        ]
        logger_error_mock.assert_called()
        logger_error_message = logger_error_mock.call_args[0][0]
        assert (
            "test_error" in logger_error_message
            and "test_error" in apm_internal_error_message
        )
        assert (
            __name__ in logger_error_message and __name__ in apm_internal_error_message
        )

    def should_return_tranformed_result_when_success_handler(self):
        expected_result = {"message": "ok"}

        class MyController(FastAPIController):
            class Config:
                success_handler = lambda result: expected_result  # noqa E731

            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()

        assert as_fastapi(result) == expected_result

    @patch.object(elasticapm, "set_custom_context")
    def should_raise_fastapi_http_exception_mapped_and_inject_info_in_apm(
        self,
        apm_set_custom_context_mock,
    ):
        http_error = HttpError(status_code=404, detail="Task not Found")

        class MyController(FastAPIController):
            class Config:
                error_map = {NotFound: http_error}

            def execute(self) -> BoolResult:
                return Failure(NotFound())

        with pytest.raises(HTTPException) as excinfo:
            result = MyController().execute()
            as_fastapi(result)

        assert excinfo.value.status_code == http_error.status_code
        assert excinfo.value.detail == http_error.detail

        apm_set_custom_context_mock.assert_called()
        apm_set_custom_context_arg = apm_set_custom_context_mock.call_args[0][0]

        assert apm_set_custom_context_arg["http_response"] == str(http_error)

    @patch.object(logger, "error")
    @patch.object(elasticapm, "set_custom_context")
    def should_logging_error_message_and_inject_it_in_apm_with_non_mapped_error(
        self, apm_set_custom_context_mock, logger_error_mock
    ):
        class MyError(DomainError):
            pass

        class MyController(FastAPIController):
            def execute(self) -> BoolResult:
                return Failure(MyError())

        with pytest.raises(HTTPException) as excinfo:
            result = MyController().execute()
            as_fastapi(result)

        assert excinfo.value.status_code == 500
        error_message = "Error 'MyError' is not mapped in controller"

        logger_error_mock.assert_called()
        logger_error_message = logger_error_mock.call_args_list[0][0]
        assert error_message in logger_error_message

        apm_set_custom_context_mock.assert_called()
        apm_set_custom_context_arg = apm_set_custom_context_mock.call_args[0][0]

        assert apm_set_custom_context_arg["internal_error_message"] == error_message

    @pytest.mark.parametrize(
        "configured_middlewares",
        [[], [PrintMiddleware], [PrintMiddleware, PrintMiddleware]],
    )
    def should_return_success_result_with_middlewares(
        self,
        configured_middlewares,
    ):
        class MyController(FastAPIController):
            class Config:
                middlewares = configured_middlewares

            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()
        assert as_fastapi(result) == FASTAPI_DEFAULT_RESPONSE

    def should_execute_middleware_when_controller_raise_an_unexpected_exception(self):
        class MyController(FastAPIController):
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
                with pytest.raises(HTTPException):
                    result = MyController().execute()
                    as_fastapi(result)

        mock_middleware_before.assert_called()
        mock_middleware_after.assert_called()

    def should_success_with_all_configurations_when_success_result(self):
        class MyController(FastAPIController):
            class Config:
                middlewares = [PrintMiddleware]
                success_handler = lambda result: FASTAPI_DEFAULT_RESPONSE  # noqa E731
                error_map = {
                    NotFound: HttpError(status_code=404, detail="Task not Found")
                }

            def execute(self) -> BoolResult:
                return isSuccess

        result = MyController().execute()
        assert as_fastapi(result) == FASTAPI_DEFAULT_RESPONSE

    @pytest.mark.parametrize(
        "result,expected_http_exception",
        [
            (isFailure, HTTPException(500, detail="Unknown Error")),
            (Failure(NotFound()), HTTPException(404, detail="Task not Found")),
            (Failure(AlreadyExists()), HTTPException(409, detail="AlreadyExists")),
            (
                Failure(
                    AlreadyExists(uuid_value="76f5994d-b16f-45b0-b3e4-e531f784f801")
                ),
                HTTPException(
                    409, detail="AlreadyExists (76f5994d-b16f-45b0-b3e4-e531f784f801)"
                ),
            ),
            (
                Failure(
                    AlreadyExists(
                        uuid_value="76f5994d-b16f-45b0-b3e4-e531f784f801",
                        additional_info={
                            "patterns": "Products",
                            "table": "UserProduct",
                        },
                    )
                ),
                HTTPException(
                    409,
                    detail="AlreadyExists (76f5994d-b16f-45b0-b3e4-e531f784f801) [{'patterns': 'Products', 'table': 'UserProduct'}]",
                ),
            ),
            (
                Failure(
                    AlreadyExists(
                        additional_info={"patterns": "Products", "table": "UserProduct"}
                    )
                ),
                HTTPException(
                    409,
                    detail="AlreadyExists [{'patterns': 'Products', 'table': 'UserProduct'}]",
                ),
            ),
        ],
    )
    def should_raise_fastapi_http_exception_with_all_configurations_when_failure_result(
        self, result, expected_http_exception
    ):
        class MyController(FastAPIController):
            class Config:
                middlewares = [PrintMiddleware]
                success_handler = lambda result: FASTAPI_DEFAULT_RESPONSE  # noqa E731
                error_map = {
                    NotFound: HttpError(status_code=404, detail="Task not Found")
                }

            def execute(self) -> BoolResult:
                return result

        with pytest.raises(HTTPException) as excinfo:
            result = MyController().execute()
            as_fastapi(result)

        assert_http_exception(excinfo.value, expected_http_exception)

    @pytest.mark.parametrize(
        "result,expected_response",
        [
            (Success(5), {"result": 5}),
            (Success("ok"), {"result": "ok"}),
            (Success(5.45), {"result": 5.45}),
            (Success([1, 2]), {"result": [1, 2]}),
            (Success((1, 2)), {"result": (1, 2)}),
            # (Success(type("MyClass", (), {})()), {"result": "<test_fastapi_controller.MyClass object at 0x106140518>"}),
        ],
    )
    def should_return_parsed_result_when_success_result_with_value(
        self, result: Result, expected_response: Dict[str, Any]
    ):
        class MyController(FastAPIController):
            def execute(self) -> Result:
                return result

        result = MyController().execute()
        assert as_fastapi(result) == expected_response

    @pytest.mark.parametrize(
        "result,expected_response",
        [
            (Success(5), FASTAPI_DEFAULT_RESPONSE),
            (Failure(), FASTAPI_DEFAULT_RESPONSE),
        ],
    )
    def should_return_default_response_overriding_failure_handler(
        self, result: Result, expected_response: Dict[str, Any]
    ):
        class MyController(FastAPIController):
            class Config:
                success_handler = lambda result: FASTAPI_DEFAULT_RESPONSE  # noqa E731
                failure_handler = lambda result: FASTAPI_DEFAULT_RESPONSE  # noqa E731
                error_map = {
                    NotFound: HttpError(status_code=404, detail="Task not Found")
                }

            def execute(self) -> BoolResult:
                return result

        result = MyController().execute()
        assert as_fastapi(result) == expected_response

    @pytest.mark.parametrize(
        "result,expected_response",
        [
            (Success(5), FASTAPI_DEFAULT_RESPONSE),
            (Failure(), FASTAPI_DEFAULT_RESPONSE),
        ],
    )
    def should_return_default_response_overriding_failure_handler_with_error_map(
        self, result: Result, expected_response: Dict[str, Any]
    ):
        class MyController(FastAPIController):
            class Config:
                success_handler = lambda result: FASTAPI_DEFAULT_RESPONSE  # noqa E731
                failure_handler = (
                    lambda result, error_map: FASTAPI_DEFAULT_RESPONSE
                )  # noqa E731
                error_map = {
                    NotFound: HttpError(status_code=404, detail="Task not Found")
                }

            def execute(self) -> BoolResult:
                return result

        result = MyController().execute()
        assert as_fastapi(result) == expected_response

    def should_succees_when_use_as_fastapi_controller_result(self):  # noqa
        class MyController(FastAPIController):
            def execute(self) -> Result[int, Error]:
                return Success(1)

        def function() -> int:
            result = MyController().execute()
            return as_fastapi(result, expected_type=int)

        function()

    def should_fail_when_return_type_is_not_a_result(self):  # noqa
        class MyController(FastAPIController):
            def execute(self) -> AnyResult:
                return 1

        with pytest.raises(TypeError, match="Controller Error"):
            MyController().execute()

    def should_return_responses_when_error_map_is_defined(self):
        class MyController(FastAPIController):
            class Config:
                error_map = {
                    NotFound: HttpError(status_code=404, detail="Task not Found")
                }

            def execute(self) -> BoolResult:
                return isSuccess

        responses = MyController.responses()
        assert responses == {404: {"description": "Task not Found"}}

    def should_return_none_responses_when_config_is_not_defined(self):
        class MyController(FastAPIController):
            def execute(self) -> BoolResult:
                return isSuccess

        responses = MyController.responses()
        assert responses is None

    def should_return_none_responses_when_error_map_is_not_defined(self):
        class MyController(FastAPIController):
            class Config:
                success_handler = lambda result: FASTAPI_DEFAULT_RESPONSE  # noqa E731

            def execute(self) -> BoolResult:
                return isSuccess

        responses = MyController.responses()
        assert responses is None
