from unittest.mock import patch

import elasticapm
import pytest
from fastapi import HTTPException
from loguru import logger
from meiga import BoolResult, Failure, Result, Success, isFailure, isSuccess

from petisco import AlreadyExists, DomainError, HttpError, NotFound, PrintMiddleware
from petisco.extra.fastapi import (
    FASTAPI_DEFAULT_RESPONSE,
    FastAPIController,
    assert_http_exception,
)


@pytest.mark.unit
def test_fastapi_controller_should_return_dict_when_success_result():
    class MyController(FastAPIController):
        def execute(self) -> BoolResult:
            return isSuccess

    result = MyController().execute()
    assert result == FASTAPI_DEFAULT_RESPONSE


@pytest.mark.unit
def test_fastapi_controller_should_raise_http_exception_when_failure_result():
    class MyController(FastAPIController):
        def execute(self) -> BoolResult:
            return isFailure

    with pytest.raises(HTTPException) as excinfo:
        MyController().execute()

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "Unknown Error"


@pytest.mark.unit
@patch.object(logger, "error")
@patch.object(elasticapm, "set_custom_context")
def test_fastapi_controller_should_logging_error_with_traceback_and_inject_in_apm(
    apm_set_custom_context_mock, logger_error_mock
):
    class MyController(FastAPIController):
        def execute(self) -> BoolResult:
            raise TypeError("test_error")

    with pytest.raises(HTTPException):
        MyController().execute()

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
    assert __name__ in logger_error_message and __name__ in apm_internal_error_message


@pytest.mark.unit
def test_fastapi_controller_should_return_mapped_success_handler():
    expected_result = {"message", "ok"}

    class MyController(FastAPIController):
        class Config:
            success_handler = lambda result: expected_result  # noqa E731

        def execute(self) -> BoolResult:
            return isSuccess

    result = MyController().execute()

    assert result == expected_result


@pytest.mark.unit
@patch.object(elasticapm, "set_custom_context")
def test_fastapi_controller_should_raise_fastapi_http_exception_mapped_and_inject_info_in_apm(
    apm_set_custom_context_mock,
):
    http_error = HttpError(status_code=404, detail="Task not Found")

    class MyController(FastAPIController):
        class Config:
            error_map = {NotFound: http_error}

        def execute(self) -> BoolResult:
            return Failure(NotFound())

    with pytest.raises(HTTPException) as excinfo:
        MyController().execute()

    assert excinfo.value.status_code == http_error.status_code
    assert excinfo.value.detail == http_error.detail

    apm_set_custom_context_mock.assert_called()
    apm_set_custom_context_arg = apm_set_custom_context_mock.call_args[0][0]

    assert apm_set_custom_context_arg["http_response"] == str(http_error)


@pytest.mark.unit
@patch.object(logger, "error")
@patch.object(elasticapm, "set_custom_context")
def test_fastapi_controller_should_logging_error_message_and_inject_it_in_apm_with_non_mapped_error(
    apm_set_custom_context_mock, logger_error_mock
):
    class MyError(DomainError):
        pass

    class MyController(FastAPIController):
        def execute(self) -> BoolResult:
            return Failure(MyError())

    with pytest.raises(HTTPException) as excinfo:
        MyController().execute()

    assert excinfo.value.status_code == 500
    error_message = "Error 'MyError' is not mapped in controller"

    logger_error_mock.assert_called()
    logger_error_message = logger_error_mock.call_args_list[0][0]
    assert error_message in logger_error_message

    apm_set_custom_context_mock.assert_called()
    apm_set_custom_context_arg = apm_set_custom_context_mock.call_args[0][0]

    assert apm_set_custom_context_arg["internal_error_message"] == error_message


@pytest.mark.unit
@pytest.mark.parametrize(
    "configured_middlewares",
    [[], [PrintMiddleware], [PrintMiddleware, PrintMiddleware]],
)
def test_fastapi_controller_should_return_success_result_with_middlewares(
    configured_middlewares,
):
    class MyController(FastAPIController):
        class Config:
            middlewares = configured_middlewares

        def execute(self) -> BoolResult:
            return isSuccess

    result = MyController().execute()
    assert result == FASTAPI_DEFAULT_RESPONSE


@pytest.mark.unit
def test_fastapi_controller_should_execute_middleware_when_controller_raise_an_unexpected_exception():
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
                MyController().execute()

    mock_middleware_before.assert_called()
    mock_middleware_after.assert_called()


@pytest.mark.unit
def test_fastapi_controller_should_success_with_all_configurations_when_success_result():
    class MyController(FastAPIController):
        class Config:
            middlewares = [PrintMiddleware]
            success_handler = lambda result: FASTAPI_DEFAULT_RESPONSE  # noqa E731
            error_map = {NotFound: HttpError(status_code=404, detail="Task not Found")}

        def execute(self) -> BoolResult:
            return isSuccess

    result = MyController().execute()
    assert result == FASTAPI_DEFAULT_RESPONSE


@pytest.mark.unit
@pytest.mark.parametrize(
    "result,expected_http_exception",
    [
        (isFailure, HTTPException(500, detail="Unknown Error")),
        (Failure(NotFound()), HTTPException(404, detail="Task not Found")),
        (Failure(AlreadyExists()), HTTPException(409, detail="AlreadyExists")),
        (
            Failure(AlreadyExists(uuid_value="76f5994d-b16f-45b0-b3e4-e531f784f801")),
            HTTPException(
                409, detail="AlreadyExists (76f5994d-b16f-45b0-b3e4-e531f784f801)"
            ),
        ),
        (
            Failure(
                AlreadyExists(
                    uuid_value="76f5994d-b16f-45b0-b3e4-e531f784f801",
                    additional_info={"patterns": "Products", "table": "UserProduct"},
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
def test_fastapi_controller_should_raise_fastapi_http_exception_with_all_configurations_when_failure_result(
    result, expected_http_exception
):
    class MyController(FastAPIController):
        class Config:
            middlewares = [PrintMiddleware]
            success_handler = lambda result: DEFAULT_RESPONSE_FASTAPI_OK  # noqa E731
            error_map = {NotFound: HttpError(status_code=404, detail="Task not Found")}

        def execute(self) -> BoolResult:
            return result

    with pytest.raises(HTTPException) as excinfo:
        MyController().execute()

    assert_http_exception(excinfo.value, expected_http_exception)


@pytest.mark.unit
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
def test_fastapi_controller_should_return_parsed_result_when_success_result_with_value(
    result, expected_response
):
    class MyController(FastAPIController):
        def execute(self) -> Result:
            return result

    result = MyController().execute()
    assert result == expected_response


@pytest.mark.unit
def test_fastapi_controller_should_raise_an_exception_if_execute_method_is_not_implemented():

    with pytest.raises(NotImplementedError) as excinfo:

        class MyController(FastAPIController):
            pass

        assert (
            excinfo.value.message
            == "Petisco Controller must implement an execute method"
        )
