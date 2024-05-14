from typing import Any, Dict

from meiga import AnyResult

from petisco.extra.fastapi.controller.fastapi_default_response import (
    FASTAPI_DEFAULT_RESPONSE,
)


def fastapi_success_handler(result: AnyResult) -> Dict[str, Any]:
    try:
        response = FASTAPI_DEFAULT_RESPONSE if result.value is True else {"result": result.value}
    except Exception:  # noqa
        response = FASTAPI_DEFAULT_RESPONSE

    return response
