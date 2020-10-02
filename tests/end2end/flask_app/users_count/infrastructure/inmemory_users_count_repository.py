from typing import Dict

from meiga import Result, Error, isSuccess, Success

from tests.end2end.flask_app.users_count.domain.interface_users_count_repository import (
    IUsersCountRepository,
)


class InMemoryUsersCountRepository(IUsersCountRepository):
    def __init__(self):
        self.num_users = 0

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def increase(self) -> Result[bool, Error]:
        self.num_users += 1
        return isSuccess

    def decrease(self) -> Result[bool, Error]:
        self.num_users -= 1
        return isSuccess

    def count(self) -> Result[int, Error]:
        return Success(self.num_users)
