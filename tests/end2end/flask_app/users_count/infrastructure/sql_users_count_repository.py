from typing import Any, Callable

from meiga import Result, Error, isSuccess, Success

from petisco import Petisco

from tests.end2end.flask_app.users_count.domain.interface_users_count_repository import (
    IUsersCountRepository,
)


class SqlUsersCountRepository(IUsersCountRepository):
    @staticmethod
    def build():
        return SqlUsersCountRepository(
            session_scope=Petisco.persistence_session_scope(),
            users_count_model=Petisco.get_persistence_model("petisco", "users_count"),
        )

    def __init__(self, session_scope: Callable, users_count_model: Any):
        self.session_scope = session_scope
        self.UsersCountModel = users_count_model

    def increase(self) -> Result[bool, Error]:
        with self.session_scope("petisco") as session:
            users_count_model = session.query(self.UsersCountModel).first()
            if not users_count_model:
                users_count_model = self.UsersCountModel(count=1)
                session.add(users_count_model)
                return isSuccess

            users_count_model.count += 1

            return isSuccess

    def decrease(self) -> Result[bool, Error]:
        with self.session_scope("petisco") as session:
            users_count_model = session.query(self.UsersCountModel).first()
            if not users_count_model:
                users_count_model = self.UsersCountModel(count=0)
                session.add(users_count_model)
                return isSuccess

            users_count_model.count -= 1

            return isSuccess

    def count(self) -> Result[int, Error]:
        with self.session_scope("petisco") as session:
            users_count_model = session.query(self.UsersCountModel).first()
            if not users_count_model:
                return Success(0)

            return Success(users_count_model.count)
