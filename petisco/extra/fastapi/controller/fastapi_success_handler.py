from meiga import Result

from petisco.extra.fastapi.controller.fastapi_default_response import (
    FASTAPI_DEFAULT_RESPONSE,
)


def fastapi_success_handler(result: Result):
    try:
        response = (
            FASTAPI_DEFAULT_RESPONSE
            if result.value is True
            else {"result": result.value}
        )
    except Exception:
        response = FASTAPI_DEFAULT_RESPONSE

    return response
