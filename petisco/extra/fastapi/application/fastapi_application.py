from typing import Callable

from fastapi import FastAPI

from petisco.base.application.application import Application
from petisco.extra.fastapi.application.add_controller_responses_to_response_mocker_dependencies import (
    add_controller_responses_to_response_mocker_dependencies,
)
from petisco.extra.fastapi.application.ensure_all_routers_are_async import (
    ensure_all_routers_are_async,
)


class FastApiApplication(Application):
    fastapi_configurer: Callable[[], FastAPI]
    ensure_async_routers: bool = False

    def get_app(self) -> FastAPI:
        app = self.fastapi_configurer()

        if self.ensure_async_routers is True:
            ensure_all_routers_are_async(app)

        add_controller_responses_to_response_mocker_dependencies(app)

        return app
