from meiga import Result

from petisco import controller_handler, TokenManager, HttpError, InfoId, UserId
from petisco.domain.value_objects.name import Name
from petisco.domain.errors.given_input_is_not_valid_error import (
    GivenInputIsNotValidError,
)
from petisco.domain.errors.given_name_is_not_valid_error import GivenNameIsNotValidError
from tests.end2end.flask_app.user.application.user_creator import UserCreator


def success_handler(result: Result):
    return {"user_id": result.value.value}, 200


class GivenInputIsNotValidHttpError(HttpError):
    def __init__(self, message: str = "Given input is not valid", code: int = 409):
        super(GivenInputIsNotValidHttpError, self).__init__(message=message, code=code)


def error_handler(result: Result):
    print(f"error_handler: {result}")
    domain_error = result.value
    if isinstance(domain_error, (GivenNameIsNotValidError, GivenInputIsNotValidError)):
        return GivenInputIsNotValidHttpError()


@controller_handler(
    success_handler=success_handler,
    error_handler=error_handler,
    token_manager=TokenManager(token_type="ADMIN_TOKEN"),
    send_request_responded_event=True,
)
def create_user(info_id: InfoId, body: dict):
    info_id.user_id = UserId.generate()

    name = Name(body.get("name"))
    return UserCreator.build().execute(info_id=info_id, name=name)
