from petisco.extra.fastapi.is_fastapi_available import is_fastapi_available

__all__ = []

if is_fastapi_available():
    from petisco.extra.fastapi.application.fastapi_application import FastApiApplication
    from petisco.extra.fastapi.application.response_mocker import ResponseMocker
    from petisco.extra.fastapi.controller.as_fastapi import as_fastapi
    from petisco.extra.fastapi.controller.async_fastapi_controller import AsyncFastAPIController
    from petisco.extra.fastapi.controller.fastapi_controller import FastAPIController
    from petisco.extra.fastapi.controller.fastapi_default_response import (
        FASTAPI_DEFAULT_RESPONSE,
    )
    from petisco.extra.fastapi.testing.assert_http_exception import (
        assert_http_exception,
    )

    __all__ = [
        "FastAPIController",
        "AsyncFastAPIController",
        "as_fastapi",
        "assert_http_exception",
        "FASTAPI_DEFAULT_RESPONSE",
        "FastApiApplication",
        "ResponseMocker",
    ]
