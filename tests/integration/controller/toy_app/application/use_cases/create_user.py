from meiga import Result, Success, Error

from petisco import UseCase, use_case_logger
from petisco.domain.entities.client_id import ClientId
from petisco.domain.entities.name import Name
from petisco.domain.entities.user_id import UserId
from tests.integration.controller.toy_app.domain.repositories.interface_user_repository import (
    IUserRepository,
)


@use_case_logger()
class CreateUser(UseCase):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, client_id: ClientId, name: Name) -> Result[UserId, Error]:
        user_id = UserId.generate().handle()
        self.user_repository.save(
            client_id=client_id, user_id=user_id, name=name
        ).handle()
        return Success(user_id)
