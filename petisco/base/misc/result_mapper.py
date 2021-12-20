from abc import ABC
from typing import Any, Callable, Dict

from meiga import Result


def default_failure_handler(result: Result, error_map: Dict):
    error_type = type(result.value)
    mapped_result = error_map.get(error_type, result)
    return mapped_result


class ResultMapper(ABC):
    def __init__(
        self,
        error_map: Dict[type, Any] = None,
        success_handler: Callable = lambda result: result,
        failure_handler: Callable = default_failure_handler,
    ):
        self.error_map = error_map if error_map is not None else dict()
        self.success_handler = success_handler
        self.failure_handler = failure_handler

    def map(self, result: Result):
        if result.is_success:
            return self.success_handler(result)
        else:
            return self.failure_handler(result, self.error_map)
