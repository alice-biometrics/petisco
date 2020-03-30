from meiga import Result, Success

from petisco import controller_handler, InfoId


def success_handler(result: Result):
    return {"result": result.value}, 200


@controller_handler(success_handler=success_handler)
def sum(headers=None, body=None):  # noqa: E501

    _ = InfoId.from_headers(headers)

    value_1 = body.get("value_1")
    value_2 = body.get("value_2")

    return Success(value_1 + value_2)
