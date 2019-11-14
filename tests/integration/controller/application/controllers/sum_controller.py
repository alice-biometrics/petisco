from meiga import Result, Success

from petisco import controller


def success_handler(result: Result):
    return {"result": result.value}, 200


@controller(success_handler=success_handler)
def sum(body=None):  # noqa: E501
    value_1 = body.get("value_1")
    value_2 = body.get("value_2")
    return Success(value_1 + value_2)
