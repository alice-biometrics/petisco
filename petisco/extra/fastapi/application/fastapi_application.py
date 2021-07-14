from typing import Callable

from fastapi import FastAPI

from petisco.base.application.application import Application


class FastApiApplication(Application):
    fastapi_configurer: Callable[[], FastAPI]

    def get_app(self) -> FastAPI:
        return self.fastapi_configurer()
