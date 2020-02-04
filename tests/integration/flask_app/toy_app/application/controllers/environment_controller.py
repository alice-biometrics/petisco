from meiga import Result, Success

from petisco import controller_handler


def success_handler(result: Result):
    return result.value, 200


@controller_handler(success_handler=success_handler)
def get_environment(headers=None):  # noqa: E501
    return Success({"uname": "Darwin"})
