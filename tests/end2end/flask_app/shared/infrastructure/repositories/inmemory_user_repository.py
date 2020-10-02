from typing import Dict

from meiga import Result, Error, isSuccess, Success, Failure

from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId
from tests.end2end.flask_app.shared.domain.repositories.interface_user_repository import (
    IUserRepository,
)
from tests.end2end.flask_app.shared.domain.repositories.user_not_found_error import (
    UserNotFoundError,
)
from tests.end2end.flask_app.user.domain.aggregate_roots.user import User


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users = {}

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def save(self, user: User) -> Result[bool, Error]:
        self.users[f"{user.client_id}_{user.user_id}"] = user
        return isSuccess

    def retrieve(self, client_id: ClientId, user_id: UserId) -> Result[User, Error]:
        if f"{client_id}_{user_id}" in self.users:
            return Success(self.users[f"{client_id}_{user_id}"])
        else:
            return Failure(UserNotFoundError())
