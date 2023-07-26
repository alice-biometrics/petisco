from typing import Optional

import pytest
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from meiga import BoolResult, Failure, isFailure, isSuccess

from petisco import DomainError, HttpError, NotFound, assert_http
from petisco.extra.fastapi import FastAPIController, as_fastapi

app = FastAPI(title="test-app")


class OtherError(DomainError):
    ...


class OtherMappedError(DomainError):
    ...


result_from_expected_behavior = {
    "success": isSuccess,
    "failure_generic": isFailure,
    "failure_not_found": Failure(NotFound()),
    "failure_other_error": Failure(OtherError()),
    "failure_other_mapped_error": Failure(OtherMappedError()),
}


class MyController(FastAPIController):
    class Config:
        error_map = {
            OtherMappedError: HttpError(status_code=401, detail="OtherMappedError")
        }

    def execute(self, expected_behavior: str) -> BoolResult:
        return result_from_expected_behavior.get(expected_behavior, isSuccess)


@app.get("/test", responses=MyController.responses())
def entry_point(x_behavior: Optional[str] = Header("success")):
    result = MyController().execute(x_behavior)
    return as_fastapi(result)


@pytest.mark.integration
@pytest.mark.parametrize(
    "behavior,expected_status_code",
    [
        ("success", 200),
        ("failure_generic", 500),
        ("failure_not_found", 404),
        ("failure_other_error", 500),
        ("failure_other_mapped_error", 401),
    ],
)
def test_fastapi_app_with_controller_and_responses_should_return_expected_values(
    behavior, expected_status_code
):
    with TestClient(app) as client:
        response = client.get("/test", headers={"x-behavior": behavior})
        assert_http(response, expected_status_code)
