from abc import ABC
from typing import Any, Callable, Optional, Union

from meiga import AnyResult, Error, Result

from petisco.base.application.controller.error_map import ErrorMap
from petisco.base.application.controller.http_error import HttpError
from petisco.base.domain.errors.domain_error import DomainError


def default_failure_handler(
    result: AnyResult, error_map: ErrorMap
) -> Union[HttpError, AnyResult]:
    error_type = type(result.value)
    mapped_result = error_map.get(error_type, result)
    return mapped_result


class ResultMapper(ABC):
    def __init__(
        self,
        error_map: Optional[ErrorMap] = None,
        success_handler: Callable[[AnyResult], Any] = lambda result: result,
        failure_handler: Callable[
            [Result[DomainError, Error], ErrorMap], Any
        ] = default_failure_handler,
    ):
        self.error_map = error_map if error_map is not None else dict()
        self.success_handler = success_handler
        self.failure_handler = failure_handler

    def map(self, result: AnyResult) -> Any:
        if result.is_success:
            return self.success_handler(result)
        else:
            return self.failure_handler(result, self.error_map)
