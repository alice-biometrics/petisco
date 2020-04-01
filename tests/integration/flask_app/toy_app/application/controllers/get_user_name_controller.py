from meiga import Result

from petisco import controller_handler, TokenManager, InfoId
from tests.integration.flask_app.toy_app.application.use_cases.use_case_builder import (
    UseCaseBuilder,
)


def success_handler(result: Result):
    return {"name": result.value}, 200


@controller_handler(
    success_handler=success_handler,
    token_manager=TokenManager(token_type="USER_TOKEN", require_user=True),
)
def get_user_name(info_id: InfoId):  # noqa: E501
    use_case = UseCaseBuilder.get_user_name()
    return use_case.execute(info_id)
