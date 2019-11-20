from typing import Dict

from meiga import Result, Error, NotImplementedMethodError

from petisco.application.repository import Repository
from petisco.domain.entities.client_id import ClientId
from petisco.domain.entities.name import Name
from petisco.domain.entities.user_id import UserId


class IUserRepository(Repository):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def save(
        self, client_id: ClientId, user_id: UserId, name: Name
    ) -> Result[bool, Error]:
        return NotImplementedMethodError

    def find_name(self, client_id: ClientId, user_id: UserId) -> Result[Name, Error]:
        return NotImplementedMethodError
