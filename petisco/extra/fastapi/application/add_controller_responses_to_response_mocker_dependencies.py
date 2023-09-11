from fastapi import FastAPI
from fastapi.routing import APIRoute

from petisco.extra.fastapi.application.response_mocker import ResponseMocker


def add_controller_responses_to_response_mocker_dependencies(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute) and route.responses:
            for depends in route.dependencies:
                if isinstance(depends.dependency, ResponseMocker):
                    depends.dependency.responses = route.responses
