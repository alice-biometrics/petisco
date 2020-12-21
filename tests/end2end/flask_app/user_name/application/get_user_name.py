from meiga import Result, Error, Success

from petisco import UseCase, use_case_handler, InfoId, Repositories
from petisco.domain.value_objects.name import Name
from tests.end2end.flask_app.shared.domain.repositories.interface_user_repository import (
    IUserRepository,
)


@use_case_handler()
class GetUserName(UseCase):
    @staticmethod
    def build():
        return GetUserName(repository=Repositories.get("user"))

    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def execute(self, info_id: InfoId) -> Result[Name, Error]:
        user = self.repository.retrieve(
            client_id=info_id.client_id, user_id=info_id.user_id
        ).unwrap_or_return()
        return Success(user.name)
