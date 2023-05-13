from __future__ import annotations

from abc import abstractmethod
from typing import Any, Generic, TypeVar, Union, cast

from meiga import Error, NotImplementedMethodError, Result

from petisco.base.application.controller.error_map import ErrorMap
from petisco.base.application.controller.meta_controller import MetaController
from petisco.base.misc.result_mapper import ResultMapper, default_failure_handler

T = TypeVar("T")

ControllerResult = Union[Result[T, Error], T]


class AsyncController(Generic[T], metaclass=MetaController):
    """
    A base class for creating async controllers.
    Inherit from this class to convert to domain the request values, configure middlewares and instantiate and execute
     a UseCase.
    """

    @staticmethod
    def get_default_mapper() -> ResultMapper:
        return ResultMapper()

    @staticmethod
    def get_config_mapper(config: dict[str, Any]) -> ResultMapper:
        return ResultMapper(
            error_map=cast(ErrorMap, getattr(config, "error_map", None)),
            success_handler=getattr(config, "success_handler", lambda result: result),
            failure_handler=getattr(config, "failure_handler", default_failure_handler),
            skip_result_mapping=getattr(config, "skip_result_mapping", False),
        )

    @abstractmethod
    async def execute(
        self, *args: tuple[str, ...], **kwargs: dict[str, Any]
    ) -> ControllerResult:
        return NotImplementedMethodError
