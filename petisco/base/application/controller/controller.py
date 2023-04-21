from __future__ import annotations

from abc import ABC, abstractmethod
from types import FunctionType
from typing import Any, Generic, TypeVar, Union, cast

from meiga import AnyResult, Error, NotImplementedMethodError, Result

from petisco.base.application.controller.error_map import ErrorMap
from petisco.base.application.middleware.middleware import Middleware
from petisco.base.misc.result_mapper import ResultMapper, default_failure_handler
from petisco.base.misc.wrapper import wrapper


def result_handler(result: Result) -> Any:
    assert isinstance(result, Result), "result_handler input must be a Result"
    return result.unwrap()


def get_mapper(bases: tuple[Any], config: dict[str, Any] | None) -> ResultMapper:
    mapper = ResultMapper()
    if config:
        for base in bases:
            method = getattr(base, "get_config_mapper", None)
            if method:
                mapper = method(config)

    else:
        for base in bases:
            method = getattr(base, "get_default_mapper", None)
            if method:
                mapper = method()

    return mapper


class MetaController(type, ABC):
    middlewares: list[Middleware] = []

    def __new__(
        mcs, name: str, bases: tuple[Any], namespace: dict[str, Any]
    ) -> MetaController:
        config = namespace.get("Config")

        mapper = get_mapper(bases, config)

        if "execute" not in namespace:
            raise NotImplementedError(
                "Petisco Controller must implement an execute method"
            )

        new_namespace = {}
        for attributeName, attribute in namespace.items():
            if isinstance(attribute, FunctionType) and attribute.__name__ == "execute":
                attribute = wrapper(attribute, name, config, mapper)
            new_namespace[attributeName] = attribute

        return super().__new__(mcs, name, bases, new_namespace)

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError


T = TypeVar("T")

ControllerResult = Union[Result[T, Error], T]


class Controller(Generic[T], metaclass=MetaController):
    """
    A base class for creating controllers.
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
    def execute(
        self, *args: tuple[str, ...], **kwargs: dict[str, Any]
    ) -> ControllerResult:
        return NotImplementedMethodError
