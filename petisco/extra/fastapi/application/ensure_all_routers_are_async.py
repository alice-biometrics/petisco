from fastapi import FastAPI
from fastapi.routing import APIRoute
from loguru import logger


def is_async_callable(route: APIRoute) -> bool:
    endpoint = route.endpoint
    import asyncio

    return bool(asyncio.iscoroutinefunction(endpoint))


def ensure_all_routers_are_async(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute) and not is_async_callable(route):
            logger.error(f"Router with {route.path} is not using async definition")
            raise SystemError(f"Router of {route.path} is not using async definition")
