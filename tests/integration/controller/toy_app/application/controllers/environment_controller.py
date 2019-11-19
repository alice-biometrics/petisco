from meiga import Result, Success

from petisco import controller


def success_handler(result: Result):
    return result.value, 200


@controller(success_handler=success_handler)
def get_environment():  # noqa: E501
    return Success({"uname": "Darwin"})
