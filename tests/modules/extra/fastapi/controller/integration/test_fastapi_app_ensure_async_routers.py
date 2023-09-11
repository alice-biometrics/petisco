from datetime import datetime

import pytest
from fastapi import FastAPI

from petisco.extra.fastapi import FastApiApplication


def fastapi_configurer() -> FastAPI:
    app = FastAPI(title="test-app")

    @app.get("/test/sync")
    def sync_entry_point():
        return {}

    @app.get("/test/async")
    async def async_entry_point():
        return {}

    return app


@pytest.mark.integration
def test_fastapi_application_default_ensure_async_routers_is_false():
    application = FastApiApplication(
        name="Test",
        version="1.0.0",
        organization="petisco",
        deployed_at=datetime.utcnow(),
        fastapi_configurer=fastapi_configurer,
    )
    application.get_app()


@pytest.mark.integration
def test_fastapi_application_ensure_async_routers_is_true():
    with pytest.raises(
        SystemError, match="Router of /test/sync is not using async definition"
    ):
        application = FastApiApplication(
            name="Test",
            version="1.0.0",
            organization="petisco",
            deployed_at=datetime.utcnow(),
            fastapi_configurer=fastapi_configurer,
            ensure_async_routers=True,
        )
        application.get_app()
