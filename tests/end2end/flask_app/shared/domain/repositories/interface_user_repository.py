from meiga import Result, Error, NotImplementedMethodError

from petisco.application.interface_repository import IRepository
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.user_id import UserId
from tests.end2end.flask_app.user.domain.aggregate_roots.user import User


class IUserRepository(IRepository):
    def save(self, user: User) -> Result[bool, Error]:
        return NotImplementedMethodError

    def retrieve(self, client_id: ClientId, user_id: UserId) -> Result[User, Error]:
        return NotImplementedMethodError
