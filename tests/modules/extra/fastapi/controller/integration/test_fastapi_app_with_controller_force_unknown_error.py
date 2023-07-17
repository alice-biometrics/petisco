import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from meiga import Error, Result, Success

from petisco import assert_http
from petisco.extra.fastapi import FastAPIController, as_fastapi

app = FastAPI(title="test-app")


class MyController(FastAPIController):
    def execute(self, num: int) -> Result[int, Error]:
        result = num / 0
        return Success(result)


@app.get("/test")
def entry_point():
    result = MyController().execute(5)
    return as_fastapi(result)


@pytest.mark.integration
def test_fastapi_app_with_controller_raise_unknown_error():
    with TestClient(app) as client:
        response = client.get("/test")
        assert_http(response, 500)
