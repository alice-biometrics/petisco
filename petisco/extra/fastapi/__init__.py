from petisco.extra.fastapi.is_fastapi_available import is_fastapi_available

__all__ = []

if is_fastapi_available():
    from petisco.extra.fastapi.controller.fastapi_controller import FastAPIController
    from petisco.extra.fastapi.testing.assert_http_exception import (
        assert_http_exception,
    )
    from petisco.extra.fastapi.controller.fastapi_default_response import (
        FASTAPI_DEFAULT_RESPONSE,
    )

    __all__ = ["FastAPIController", "assert_http_exception", "FASTAPI_DEFAULT_RESPONSE"]
