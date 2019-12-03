from typing import Dict

from meiga import Result, Error, isSuccess, Success, Failure

from petisco.application.repository import Repository
from petisco.domain.entities.client_id import ClientId
from petisco.domain.entities.name import Name
from petisco.domain.entities.user_id import UserId
from tests.integration.flask_app.toy_app.domain.repositories.user_not_found_error import (
    UserNotFoundError,
)


class InMemoryUserRepository(Repository):
    def __init__(self):
        self.users = {}

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def save(
        self, client_id: ClientId, user_id: UserId, name: Name
    ) -> Result[bool, Error]:
        self.users[f"{client_id}_{user_id}"] = name
        return isSuccess

    def find_name(self, client_id: ClientId, user_id: UserId) -> Result[Name, Error]:
        if f"{client_id}_{user_id}" in self.users:
            return Success(self.users[f"{client_id}_{user_id}"])
        else:
            return Failure(UserNotFoundError())
