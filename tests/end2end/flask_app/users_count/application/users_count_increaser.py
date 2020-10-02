from meiga import Result, Error

from petisco import UseCase, use_case_handler, Petisco
from tests.end2end.flask_app.users_count.domain.interface_users_count_repository import (
    IUsersCountRepository,
)


@use_case_handler()
class UserCountIncreaser(UseCase):
    @staticmethod
    def build():
        return UserCountIncreaser(repository=Petisco.get_repository("users_count"))

    def __init__(self, repository: IUsersCountRepository):
        self.repository = repository

    def execute(self) -> Result[bool, Error]:
        return self.repository.increase()
