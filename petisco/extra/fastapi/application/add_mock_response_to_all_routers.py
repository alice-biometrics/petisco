from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute

from petisco.extra.fastapi.application.response_mocker import ResponseMocker


def add_mock_response_to_all_routers(app: FastAPI, header_key: str) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            mocker = ResponseMocker(header_key=header_key, responses=route.responses)
            route.dependencies.append(Depends(mocker))
