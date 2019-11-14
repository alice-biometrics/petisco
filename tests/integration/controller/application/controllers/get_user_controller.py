from meiga import Result, Success

from petisco import controller, JwtConfig


def success_handler(result: Result):
    return {"user_id": result.value}, 200


@controller(
    success_handler=success_handler,
    jwt_config=JwtConfig(token_type="USER_TOKEN", require_user=True),
)
def get_user(client_id, user_id, *args, **kwargs):  # noqa: E501
    return Success(user_id)
