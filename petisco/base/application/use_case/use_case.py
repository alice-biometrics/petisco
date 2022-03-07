from abc import ABC, abstractmethod
from functools import wraps
from types import FunctionType
from typing import Any

import elasticapm
from meiga import Error, Failure, NotImplementedMethodError, Result
from meiga.on_failure_exception import OnFailureException

from petisco.base.application.use_case.use_case_uncontrolled_error import (
    UseCaseUncontrolledError,
)


def wrapper(method, wrapped_class_name):
    @wraps(method)
    def wrapped(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except OnFailureException as exception:
            return exception.result
        except Error as error:
            return Failure(error)
        except Exception as exception:
            uncontrolled_error = UseCaseUncontrolledError.from_exception(
                exception=exception, arguments=args, class_name=wrapped_class_name
            )
            client = elasticapm.get_client()
            if client:
                client.capture_exception()

            return Failure(uncontrolled_error)

    return wrapped


class MetaUseCase(type, ABC):
    def __new__(mcs, name, bases, namespace):
        new_class_dict = {}
        if "execute" not in namespace:
            raise NotImplementedError(
                "Petisco UseCase must implement an execute method"
            )

        for attributeName, attribute in namespace.items():
            if isinstance(attribute, FunctionType) and attribute.__name__ == "execute":
                attribute = wrapper(attribute, name)
            new_class_dict[attributeName] = attribute
        return type.__new__(mcs, name, bases, new_class_dict)

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result[Any, Error]:
        return NotImplementedMethodError


class UseCase(metaclass=MetaUseCase):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Result[Any, Error]:
        return NotImplementedMethodError
