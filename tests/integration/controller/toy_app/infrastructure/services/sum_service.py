from typing import Dict

from meiga import Result, Error, Success

from tests.integration.controller.toy_app.domain.services.interface_sum_service import (
    ISumService,
)


class SumService(ISumService):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def execute(self, value1: int, value2: int) -> Result[int, Error]:
        return Success(value1 + value2)
