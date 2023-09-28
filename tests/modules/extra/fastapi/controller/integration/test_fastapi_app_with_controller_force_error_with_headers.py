import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from meiga import BoolResult, Failure

from petisco import DomainError, HttpError, assert_http
from petisco.extra.fastapi import FastAPIController, as_fastapi

app = FastAPI(title="test-app")


class AuthFail(DomainError):
    def get_specific_detail(self) -> str:
        return "Auth Fail"


class MyController(FastAPIController):
    class Config:
        error_map = {
            AuthFail: HttpError(
                status_code=401,
                detail="Unauthorized",
                headers={"WWW-Authenticate": 'authType="OTP"'},
            )
        }

    def execute(self) -> BoolResult:
        return Failure(AuthFail())


@app.get("/test")
def entry_point():
    result = MyController().execute()
    return as_fastapi(result)


@pytest.mark.integration
def test_fastapi_app_with_controller_should_return_expected_values():
    with TestClient(app) as client:
        response = client.get("/test")
        assert_http(response, 401)
        assert response.json() == {"detail": "Unauthorized"}
        assert response.headers == {
            "www-authenticate": 'authType="OTP"',
            "content-length": "25",
            "content-type": "application/json",
        }
