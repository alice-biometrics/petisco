from typing import Dict

from meiga import Result, Error, NotImplementedMethodError

from petisco.application.repository import Repository
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId
from tests.integration.flask_app.toy_app.domain.aggregate_roots.user import User


class IUserRepository(Repository):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def save(self, user: User) -> Result[bool, Error]:
        return NotImplementedMethodError

    def find(self, client_id: ClientId, user_id: UserId) -> Result[User, Error]:
        return NotImplementedMethodError
