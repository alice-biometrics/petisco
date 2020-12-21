from typing import Any, Callable

from meiga import Result, Error, isSuccess, Success

from petisco import Persistence

from tests.end2end.flask_app.users_count.domain.interface_users_count_repository import (
    IUsersCountRepository,
)


class SqlUsersCountRepository(IUsersCountRepository):
    @staticmethod
    def build():
        return SqlUsersCountRepository(
            session_scope=Persistence.get_session_scope("petisco-sql"),
            users_count_model=Persistence.get_model("petisco-sql", "users_count"),
        )

    def __init__(self, session_scope: Callable, users_count_model: Any):
        self.session_scope = session_scope
        self.UsersCountModel = users_count_model

    def increase(self) -> Result[bool, Error]:
        with self.session_scope() as session:
            users_count_model = session.query(self.UsersCountModel).first()
            if not users_count_model:
                users_count_model = self.UsersCountModel(count=1)
                session.add(users_count_model)
                return isSuccess

            users_count_model.count += 1

            return isSuccess

    def decrease(self) -> Result[bool, Error]:
        with self.session_scope() as session:
            users_count_model = session.query(self.UsersCountModel).first()
            if not users_count_model:
                users_count_model = self.UsersCountModel(count=0)
                session.add(users_count_model)
                return isSuccess

            users_count_model.count -= 1

            return isSuccess

    def count(self) -> Result[int, Error]:
        with self.session_scope() as session:
            users_count_model = session.query(self.UsersCountModel).first()
            if not users_count_model:
                return Success(0)

            return Success(users_count_model.count)
