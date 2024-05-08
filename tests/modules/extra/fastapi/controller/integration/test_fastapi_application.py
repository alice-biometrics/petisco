from datetime import datetime, timezone

import pytest
from fastapi import Depends, FastAPI
from meiga import BoolResult, isSuccess
from starlette.testclient import TestClient

from petisco import HttpError
from petisco.extra.fastapi import (
    FastApiApplication,
    FastAPIController,
    ResponseMocker,
    as_fastapi,
)
from tests.modules.extra.fastapi.controller.integration.test_fastapi_app_with_controller import (
    OtherMappedError,
)


class MyController(FastAPIController):
    class Config:
        error_map = {OtherMappedError: HttpError(status_code=425, detail="OtherMappedError")}

    def execute(self) -> BoolResult:
        return isSuccess


def fastapi_configurer() -> FastAPI:
    app = FastAPI(title="test-app", dependencies=[Depends(ResponseMocker())])

    @app.get("/test/sync")
    def sync_entry_point():
        return {}

    @app.get("/test/async")
    async def async_entry_point():
        return {}

    @app.get("/test/controller", responses=MyController.responses())
    async def controller_entry_point():
        return as_fastapi(MyController().execute())

    return app


@pytest.mark.integration
class TestFastapiApplication:
    def should_success_when_ensure_async_routers_is_false(self):
        application = FastApiApplication(
            name="Test",
            version="1.0.0",
            organization="petisco",
            deployed_at=datetime.now(timezone.utc),
            fastapi_configurer=fastapi_configurer,
        )
        application.get_app()

    def should_raise_an_errror_when_ensure_async_routers_is_true(self):
        with pytest.raises(SystemError, match="Router of /test/sync is not using async definition"):
            application = FastApiApplication(
                name="Test",
                version="1.0.0",
                organization="petisco",
                deployed_at=datetime.now(timezone.utc),
                fastapi_configurer=fastapi_configurer,
                ensure_async_routers=True,
            )
            application.get_app()

    def should_success_when_use_mock_response_with_expected_status_code(self):
        application = FastApiApplication(
            name="Test",
            version="1.0.0",
            organization="petisco",
            deployed_at=datetime.now(timezone.utc),
            fastapi_configurer=fastapi_configurer,
        )
        app = application.get_app()

        expected_status_code = 404
        with TestClient(app) as client:
            response = client.get(
                "/test/async",
                headers={"X-Status-Code-Mock-Response": str(expected_status_code)},
            )
            assert response.status_code == expected_status_code
            assert response.json().get("detail", {}).get("is_mocked") is True

    def should_success_when_use_mock_response_with_expected_status_code_and_controller_responses(
        self,
    ):
        application = FastApiApplication(
            name="Test",
            version="1.0.0",
            organization="petisco",
            deployed_at=datetime.now(timezone.utc),
            fastapi_configurer=fastapi_configurer,
        )
        app = application.get_app()

        expected_status_code = 425
        with TestClient(app) as client:
            response = client.get(
                "/test/controller",
                headers={"X-Status-Code-Mock-Response": str(expected_status_code)},
            )
            assert response.status_code == expected_status_code
            assert response.json() == {"detail": {"description": "OtherMappedError", "is_mocked": True}}
