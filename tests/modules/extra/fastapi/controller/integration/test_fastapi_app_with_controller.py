from typing import Optional

import pytest
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from meiga import BoolResult, Failure, isFailure, isSuccess

from petisco import NotFound, assert_http
from petisco.extra.fastapi import FastAPIController

app = FastAPI(title="test-app")

result_from_expected_behavior = {
    "success": isSuccess,
    "failure_generic": isFailure,
    "failure_not_found": Failure(NotFound()),
}


class MyController(FastAPIController):
    def execute(self, expected_behavior: str) -> BoolResult:
        return result_from_expected_behavior.get(expected_behavior, isSuccess)


@app.get("/test")
def entry_point(x_behavior: Optional[str] = Header("success")):
    return MyController().execute(x_behavior)


@pytest.mark.unit
@pytest.mark.parametrize(
    "behavior,expected_status_code",
    [("success", 200), ("failure_generic", 500), ("failure_not_found", 404)],
)
def test_fastapi_app_with_controller_should_return_expected_values(
    behavior, expected_status_code
):
    with TestClient(app) as client:
        response = client.get("/test", headers={"x-behavior": behavior})
        assert_http(response, expected_status_code)
