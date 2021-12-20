from petisco.base.domain.errors.default_http_error_map import DEFAULT_HTTP_ERROR_MAP
from petisco.base.misc.result_mapper import ResultMapper
from petisco.extra.fastapi.controller.fastapi_failure_handler import (
    fastapi_failure_handler,
)
from petisco.extra.fastapi.controller.fastapi_success_handler import (
    fastapi_success_handler,
)


class FastAPIResultMapper:
    @staticmethod
    def default():
        return ResultMapper(
            error_map=DEFAULT_HTTP_ERROR_MAP,
            success_handler=fastapi_success_handler,
            failure_handler=fastapi_failure_handler,
        )

    @staticmethod
    def from_config(config):
        error_map = getattr(config, "error_map", DEFAULT_HTTP_ERROR_MAP)
        error_map = {**DEFAULT_HTTP_ERROR_MAP, **error_map}
        return ResultMapper(
            error_map=error_map,
            success_handler=getattr(config, "success_handler", fastapi_success_handler),
            failure_handler=fastapi_failure_handler,
        )
