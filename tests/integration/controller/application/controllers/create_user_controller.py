from meiga import Result, isSuccess

from petisco import controller, JwtConfig


def success_handler(result: Result):
    return {"user_created": result.value}, 200


@controller(
    success_handler=success_handler, jwt_config=JwtConfig(token_type="ADMIN_TOKEN")
)
def create_user(client_id, *args, **kwargs):  # noqa: E501
    return isSuccess
