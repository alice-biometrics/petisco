from meiga import Result, Error

from petisco import UseCase, use_case_handler, Repositories
from tests.end2end.flask_app.users_count.domain.interface_users_count_repository import (
    IUsersCountRepository,
)


@use_case_handler()
class UsersCountRetriever(UseCase):
    @staticmethod
    def build():
        return UsersCountRetriever(repository=Repositories.get("users_count"))

    def __init__(self, repository: IUsersCountRepository):
        self.repository = repository

    def execute(self) -> Result[int, Error]:
        return self.repository.count()
