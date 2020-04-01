from meiga import Result, Success

from petisco import controller_handler


def success_handler(result: Result):
    return result.value, 200


@controller_handler(success_handler=success_handler)
def get_environment():
    return Success({"uname": "Darwin"})
