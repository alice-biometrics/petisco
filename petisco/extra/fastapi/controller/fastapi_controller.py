from abc import abstractmethod
from typing import Any, Dict

from meiga import AnyResult, NotImplementedMethodError

from petisco.base.application.controller.controller import Controller
from petisco.base.misc.result_mapper import ResultMapper
from petisco.extra.fastapi.controller.fastapi_result_mapper import FastAPIResultMapper


class FastAPIController(Controller):
    @staticmethod
    def get_default_mapper() -> ResultMapper:
        return FastAPIResultMapper.default()

    @staticmethod
    def get_config_mapper(config: Dict[str, Any]) -> ResultMapper:
        return FastAPIResultMapper.from_config(config)

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> AnyResult:
        return NotImplementedMethodError
