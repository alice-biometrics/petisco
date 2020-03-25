from meiga import Result, Error, Success

from petisco import UseCase, use_case_handler
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from tests.integration.flask_app.toy_app.domain.repositories.interface_user_repository import (
    IUserRepository,
)


@use_case_handler()
class GetUserName(UseCase):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, client_id: ClientId, user_id: UserId) -> Result[Name, Error]:
        user = self.user_repository.find(
            client_id=client_id, user_id=user_id
        ).unwrap_or_return()
        return Success(user.name)
