from meiga import Result, Error, Success

from petisco import UseCase, use_case_handler
from petisco.domain.entities.client_id import ClientId
from petisco.domain.entities.name import Name
from petisco.domain.entities.user_id import UserId
from tests.integration.controller.toy_app.domain.repositories.interface_user_repository import (
    IUserRepository,
)


@use_case_handler()
class GetUserName(UseCase):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, client_id: ClientId, user_id: UserId) -> Result[Name, Error]:
        name = self.user_repository.find_name(
            client_id=client_id, user_id=user_id
        ).handle()
        return Success(name)
