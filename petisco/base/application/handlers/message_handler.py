from abc import ABC, abstractmethod
from functools import wraps
from types import FunctionType
from typing import Any, Callable, Dict, Tuple

from meiga import AnyResult, Error, Failure, NotImplementedMethodError
from meiga.on_failure_exception import OnFailureException

from petisco.base.application.use_case.use_case_uncontrolled_error import (
    UseCaseUncontrolledError,
)


def wrapper(method: Callable[..., AnyResult]) -> Callable[..., Any]:
    @wraps(method)
    def wrapped(*args: Any, **kwargs: Any) -> AnyResult:
        try:
            return method(*args, **kwargs)
        except OnFailureException as exception:
            return exception.result
        except Error as error:
            return Failure(error)
        except Exception as exception:
            return Failure(UseCaseUncontrolledError(exception))

    return wrapped


class MetaUseCase(type, ABC):
    def __new__(mcs, name: str, bases: Tuple[Any], namespace: Dict[str, Any]) -> "MetaUseCase":
        new_class_dict = {}
        if "execute" not in namespace:
            raise NotImplementedError("Petisco UseCase must implement an execute method")

        for attributeName, attribute in namespace.items():
            if isinstance(attribute, FunctionType) and attribute.__name__ == "execute":
                attribute = wrapper(attribute)
            new_class_dict[attributeName] = attribute
        return type.__new__(mcs, name, bases, new_class_dict)

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError


class UseCase(metaclass=MetaUseCase):
    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError
