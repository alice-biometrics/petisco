from abc import abstractmethod
from typing import Any

from meiga import Error, NotImplementedMethodError, Result

from petisco.base.application.controller.controller import Controller
from petisco.extra.fastapi.controller.fastapi_result_mapper import FastAPIResultMapper


class FastAPIController(Controller):
    @staticmethod
    def get_default_mapper():
        return FastAPIResultMapper.default()

    @staticmethod
    def get_config_mapper(config):
        return FastAPIResultMapper.from_config(config)

    @abstractmethod
    def execute(self, *args, **kwargs) -> Result[Any, Error]:
        return NotImplementedMethodError
