from meiga import Result, isSuccess

from petisco import controller_handler


def success_handler(result: Result):
    return {"status": "OK", "value": result.value}, 200


@controller_handler(success_handler=success_handler)
def get_healthcheck(headers=None):  # noqa: E501
    return isSuccess
