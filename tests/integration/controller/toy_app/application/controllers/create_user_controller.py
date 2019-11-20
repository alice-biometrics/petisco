from meiga import Result

from petisco import controller, JwtConfig
from tests.integration.controller.toy_app.application.use_cases.use_case_builder import (
    UseCaseBuilder,
)


def success_handler(result: Result):
    return {"user_id": result.value}, 200


@controller(
    success_handler=success_handler, jwt_config=JwtConfig(token_type="ADMIN_TOKEN")
)
def create_user(client_id, body, *args, **kwargs):  # noqa: E501
    name = body.get("name")
    use_case = UseCaseBuilder.create_user()
    return use_case.execute(client_id=client_id, name=name)
