import pytest
from fastapi import HTTPException
from meiga import BoolResult, Failure, Result, Success, isFailure, isSuccess
from petisco import HttpError
from petisco import AlreadyExists, NotFound, PrintMiddleware

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
def test_fastapi_controller_should_raise_fastapi_http_exception_mapped_by_error_map():
    class MyController(FastAPIController):
        class Config:
            error_map = {NotFound: HttpError(status_code=404, detail="Task not Found")}

        def execute(self) -> BoolResult:
            return Failure(NotFound())

    with pytest.raises(HTTPException) as excinfo:
        MyController().execute()

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Task not Found"


@pytest.mark.unit
@pytest.mark.parametrize(
    "configured_middlewares",
    [[], [PrintMiddleware], [PrintMiddleware, PrintMiddleware]],
)
def test_fastapi_controller_should_return_success_result_with_middlewares(
    configured_middlewares
):
    class MyController(FastAPIController):
        class Config:
            middlewares = configured_middlewares

        def execute(self) -> BoolResult:
            return isSuccess

    result = MyController().execute()
    assert result == FASTAPI_DEFAULT_RESPONSE


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
        (Failure(AlreadyExists()), HTTPException(409, detail="Already Exists")),
        (
            Failure(AlreadyExists(uuid_value="76f5994d-b16f-45b0-b3e4-e531f784f801")),
            HTTPException(
                409, detail="Already Exists (76f5994d-b16f-45b0-b3e4-e531f784f801)"
            ),
        ),
        (
            Failure(
                AlreadyExists(
                    uuid_value="76f5994d-b16f-45b0-b3e4-e531f784f801",
                    additional_info={"repository": "Products", "table": "UserProduct"},
                )
            ),
            HTTPException(
                409,
                detail="Already Exists (76f5994d-b16f-45b0-b3e4-e531f784f801) [{'repository': 'Products', 'table': 'UserProduct'}]",
            ),
        ),
        (
            Failure(
                AlreadyExists(
                    additional_info={"repository": "Products", "table": "UserProduct"}
                )
            ),
            HTTPException(
                409,
                detail="Already Exists [{'repository': 'Products', 'table': 'UserProduct'}]",
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