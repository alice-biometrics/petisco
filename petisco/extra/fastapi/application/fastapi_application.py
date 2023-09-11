from typing import Callable

from fastapi import FastAPI

from petisco.base.application.application import Application
from petisco.extra.fastapi.application.add_mock_response_to_all_routers import (
    add_mock_response_to_all_routers,
)
from petisco.extra.fastapi.application.ensure_all_routers_are_async import (
    ensure_all_routers_are_async,
)


class FastApiApplication(Application):
    fastapi_configurer: Callable[[], FastAPI]
    ensure_async_routers: bool = False
    use_mock_response: bool = False
    mock_response_header_key: str = "X-Status-Code-Mock-Response"

    def get_app(self) -> FastAPI:
        app = self.fastapi_configurer()

        if self.ensure_async_routers is True:
            ensure_all_routers_are_async(app)

        if self.use_mock_response:
            add_mock_response_to_all_routers(
                app=app, header_key=self.mock_response_header_key
            )

        return app
