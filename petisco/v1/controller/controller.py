from abc import ABC, abstractmethod
from functools import wraps
from inspect import signature
from types import FunctionType
from typing import List, Any

from meiga import Error, Failure, NotImplementedMethodError, Result
from meiga.on_failure_exception import OnFailureException

from petisco.v1.controller.result_mapper import ResultMapper, default_failure_handler


def wrapper(execute_func, wrapped_class_name, config, mapper):
    @wraps(execute_func)
    def wrapped(*args, **kwargs):
        middlewares_classes = getattr(config, "middlewares", [])

        arguments = signature(execute_func).bind(*args, **kwargs).arguments
        arguments.pop("self")
        middlewares = [
            klass(wrapped_class_name, arguments) for klass in middlewares_classes
        ]

        for middleware in middlewares:
            middleware.before()

        try:
            result = execute_func(*args, **kwargs)
        except OnFailureException as exc:
            result = exc.result
        except Error as error:
            result = Failure(error)

        mapped_result = mapper.map(result)
        for middleware in middlewares:
            if result:
                middleware.after(result)
        return mapped_result

    return wrapped


def get_mapper(bases, config):
    mapper = ResultMapper()
    if config:
        for base in bases:
            method = getattr(base, "get_config_mapper", None)
            if method:
                mapper = method(config)

        success_handler = getattr(config, "success_handler", None)
        if success_handler:
            mapper.success_handler = success_handler

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
    def get_config_mapper(config):
        return ResultMapper(
            error_map=getattr(config, "error_map", None),
            success_handler=getattr(config, "success_handler", lambda result: result),
            failure_handler=default_failure_handler,
        )

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result[Any, Error]:
        return NotImplementedMethodError
