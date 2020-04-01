from meiga import Result, Success

from petisco import controller_handler


def success_handler(result: Result):
    return {"result": result.value}, 200


@controller_handler(success_handler=success_handler)
def sum(body):  # noqa: E501

    value_1 = body.get("value_1")
    value_2 = body.get("value_2")

    return Success(value_1 + value_2)
