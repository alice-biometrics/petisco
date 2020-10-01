from meiga import Result

from petisco import controller_handler, TokenManager, InfoId
from tests.end2end.flask_app.user_name.application.get_user_name import GetUserName


def success_handler(result: Result):
    return {"name": result.value.value}, 200


@controller_handler(
    success_handler=success_handler,
    token_manager=TokenManager(token_type="USER_TOKEN", require_user=True),
)
def get_user_name(info_id: InfoId):
    return GetUserName.build().execute(info_id)
