from meiga import Result

from petisco import controller_handler
from tests.end2end.flask_app.sum.infrastructure.sum_executor import SumExecutor


def success_handler(result: Result):
    return {"result": result.value}, 200


@controller_handler(success_handler=success_handler)
def sum(body):

    value_1 = body.get("value_1")
    value_2 = body.get("value_2")

    return SumExecutor().execute(value_1, value_2)
