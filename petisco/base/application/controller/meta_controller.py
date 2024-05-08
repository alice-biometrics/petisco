from __future__ import annotations

from abc import ABC, abstractmethod
from inspect import iscoroutinefunction
from types import FunctionType
from typing import Any

from meiga import AnyResult, NotImplementedMethodError

from petisco.base.application.middleware.middleware import Middleware
from petisco.base.misc.async_wrapper import async_wrapper
from petisco.base.misc.result_mapper import ResultMapper
from petisco.base.misc.wrapper import wrapper


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
    use_global_middlewares: bool = True

    def __new__(mcs, name: str, bases: tuple[Any], namespace: dict[str, Any]) -> MetaController:
        config = namespace.get("Config")

        mapper = get_mapper(bases, config)

        if "execute" not in namespace:
            raise NotImplementedError("Petisco Controller must implement an execute method")

        new_namespace = {}
        for attributeName, attribute in namespace.items():
            if isinstance(attribute, FunctionType) and attribute.__name__ == "execute":
                if iscoroutinefunction(attribute):
                    attribute = async_wrapper(attribute, name, config, mapper)
                else:
                    attribute = wrapper(attribute, name, config, mapper)
            new_namespace[attributeName] = attribute

        return super().__new__(mcs, name, bases, new_namespace)

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError
