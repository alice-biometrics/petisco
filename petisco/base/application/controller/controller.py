from __future__ import annotations

from abc import abstractmethod
from typing import Any, cast

from meiga import AnyResult, NotImplementedMethodError

from petisco.base.application.application_info import ApplicationInfo
from petisco.base.application.controller.error_map import ErrorMap
from petisco.base.application.controller.meta_controller import MetaController
from petisco.base.domain.errors.default_http_error_map import DEFAULT_HTTP_ERROR_MAP
from petisco.base.misc.result_mapper import ResultMapper, default_failure_handler


def get_shared_and_default_error_map() -> ErrorMap:
    # This mapping will give preference to shared_error_map over DEFAULT_HTTP_ERROR_MAP
    shared_and_default_error_map = {
        **DEFAULT_HTTP_ERROR_MAP,
        **ApplicationInfo().shared_error_map,
    }
    return shared_and_default_error_map


class Controller(metaclass=MetaController):
    """
    A base class for creating controllers.
    Inherit from this class to convert to domain the request values,
    configure middlewares and instantiate and execute a UseCase.
    """

    @staticmethod
    def get_default_mapper() -> ResultMapper:
        error_map = get_shared_and_default_error_map()
        return ResultMapper(error_map=error_map)

    @staticmethod
    def get_config_mapper(config: dict[str, Any]) -> ResultMapper:
        shared_and_default_error_map = get_shared_and_default_error_map()
        controller_error_map = cast(ErrorMap, getattr(config, "error_map", {}))

        # This merged_dependencies will give preference to controller_error_map (given in the controller) over
        # shared_and_default_error_map
        error_map = {
            **shared_and_default_error_map,
            **controller_error_map,
        }

        return ResultMapper(
            error_map=error_map,
            success_handler=getattr(config, "success_handler", lambda result: result),
            failure_handler=getattr(config, "failure_handler", default_failure_handler),
        )

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError
