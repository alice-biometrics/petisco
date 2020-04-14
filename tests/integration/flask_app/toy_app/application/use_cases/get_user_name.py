from meiga import Result, Error, Success

from petisco import UseCase, use_case_handler, InfoId
from petisco.domain.value_objects.name import Name
from tests.integration.flask_app.toy_app.domain.repositories.interface_user_repository import (
    IUserRepository,
)


@use_case_handler()
class GetUserName(UseCase):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, info_id: InfoId) -> Result[Name, Error]:
        user = self.user_repository.retrieve(
            client_id=info_id.client_id, user_id=info_id.user_id
        ).unwrap_or_return()
        return Success(user.name)
