from typing import Optional

import pytest
from fastapi import FastAPI, Header
from fastapi.testclient import TestClient
from meiga import Error, Result

from petisco import BusCannotPublish, CriticalError, assert_http
from petisco.extra.fastapi import FastAPIController, as_fastapi

app = FastAPI(title="test-app")

result_from_expected_behavior = {"default": CriticalError(), "bus": BusCannotPublish()}


class MyController(FastAPIController):
    def execute(self, critical_error: CriticalError) -> Result[int, Error]:
        raise critical_error


@app.get("/test")
def entry_point(x_behavior: Optional[str] = Header("default")):
    error = result_from_expected_behavior.get(x_behavior)
    result = MyController().execute(error)
    return as_fastapi(result)


@pytest.mark.integration
@pytest.mark.parametrize("behavior", ["default", "bus"])
def test_fastapi_app_with_controller_raise_critical_error(behavior: str):
    with TestClient(app) as client:
        response = client.get("/test", headers={"x-behavior": behavior})
        assert_http(response, 500)
