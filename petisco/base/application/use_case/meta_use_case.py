from abc import ABC, abstractmethod
from functools import wraps
from inspect import iscoroutinefunction, signature
from types import FunctionType
from typing import Any, Callable, Dict, Tuple

from meiga import AnyResult, Error, Failure, NotImplementedMethodError

from petisco.base.application.use_case.use_case_uncontrolled_error import (
    UseCaseUncontrolledError,
)
from petisco.extra.elastic_apm.capture_exception import capture_exception
from petisco.extra.meiga import WaitingForEarlyReturn


def use_case_wrapper(method: Callable[..., AnyResult], wrapped_class_name: str) -> Callable[..., AnyResult]:
    @wraps(method)
    def wrapped(*args: Any, **kwargs: Any) -> AnyResult:
        try:
            return method(*args, **kwargs)
        except WaitingForEarlyReturn as exception:
            return exception.result
        except Error as error:
            return Failure(error)
        except Exception as exception:
            arguments = signature(method).bind(*args, **kwargs).arguments
            arguments.pop("self")
            uncontrolled_error = UseCaseUncontrolledError.from_exception(
                exception=exception, arguments=arguments, class_name=wrapped_class_name
            )
            capture_exception()

            return Failure(uncontrolled_error)

    return wrapped


def async_use_case_wrapper(
    method: Callable[..., AnyResult], wrapped_class_name: str
) -> Callable[..., AnyResult]:
    @wraps(method)
    async def wrapped(*args: Any, **kwargs: Any) -> AnyResult:
        try:
            return await method(*args, **kwargs)
        except WaitingForEarlyReturn as exception:
            return exception.result
        except Error as error:
            return Failure(error)
        except Exception as exception:
            arguments = signature(method).bind(*args, **kwargs).arguments
            arguments.pop("self")
            uncontrolled_error = UseCaseUncontrolledError.from_exception(
                exception=exception, arguments=arguments, class_name=wrapped_class_name
            )
            capture_exception()
            return Failure(uncontrolled_error)

    return wrapped


class MetaUseCase(type, ABC):
    def __new__(mcs, name: str, bases: Tuple[Any], namespace: Dict[str, Any]) -> "MetaUseCase":
        new_class_dict = {}
        if "execute" not in namespace:
            raise NotImplementedError("Petisco UseCase or AsyncUseCase must implement an execute method")

        for attributeName, attribute in namespace.items():
            if isinstance(attribute, FunctionType) and attribute.__name__ == "execute":
                if iscoroutinefunction(attribute):
                    attribute = async_use_case_wrapper(attribute, name)
                else:
                    attribute = use_case_wrapper(attribute, name)
            new_class_dict[attributeName] = attribute
        return type.__new__(mcs, name, bases, new_class_dict)

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError
