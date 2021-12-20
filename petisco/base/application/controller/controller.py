from abc import ABC, abstractmethod
from types import FunctionType
from typing import Any, List

from meiga import Error, NotImplementedMethodError, Result

from petisco.base.misc.result_mapper import ResultMapper, default_failure_handler
from petisco.base.misc.wrapper import wrapper


def get_mapper(bases, config):
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
    middlewares: List = {}

    def __new__(mcs, name, bases, namespace):
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
    def execute(self, *args, **kwargs) -> Result[Any, Error]:
        return NotImplementedMethodError


class Controller(metaclass=MetaController):
    @staticmethod
    def get_default_mapper() -> ResultMapper:
        return ResultMapper()

    @staticmethod
    def get_config_mapper(config):
        return ResultMapper(
            error_map=getattr(config, "error_map", None),
            success_handler=getattr(config, "success_handler", lambda result: result),
            failure_handler=default_failure_handler,
        )

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result[Any, Error]:
        return NotImplementedMethodError
