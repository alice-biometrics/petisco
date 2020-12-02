from meiga import Result, Error, Success

from tests.end2end.flask_app.sum.domain.interface_sum_executor import ISumExecutor


class SumExecutor(ISumExecutor):
    def execute(self, value1: int, value2: int) -> Result[int, Error]:
        return Success(value1 + value2)
