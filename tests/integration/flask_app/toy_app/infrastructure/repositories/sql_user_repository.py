from typing import Dict, Any, Callable

from meiga import Result, Error, isSuccess, Success, Failure

from petisco import Petisco
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from tests.integration.flask_app.toy_app.domain.aggregate_roots.user import User
from tests.integration.flask_app.toy_app.domain.repositories.interface_user_repository import (
    IUserRepository,
)
from tests.integration.flask_app.toy_app.domain.repositories.user_already_exist_error import (
    UserAlreadyExistError,
)
from tests.integration.flask_app.toy_app.domain.repositories.user_not_found_error import (
    UserNotFoundError,
)


class SqlUserRepository(IUserRepository):
    @staticmethod
    def build():
        return SqlUserRepository(
            session_scope=Petisco.persistence_session_scope(),
            user_model=Petisco.get_persistence_model("user"),
        )

    def __init__(self, session_scope: Callable, user_model: Any):
        self.session_scope = session_scope
        self.UserModel = user_model

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def save(self, user: User) -> Result[bool, Error]:

        result = self.exists(user.user_id)
        if result.is_success:
            return Failure(UserAlreadyExistError(user.user_id))

        with self.session_scope() as session:
            user = self.UserModel(
                client_id=user.client_id.value,
                user_id=user.user_id.value,
                name=user.name.value,
            )
            session.add(user)
        return isSuccess

    def retrieve(self, client_id: ClientId, user_id: UserId) -> Result[User, Error]:

        with self.session_scope() as session:
            user_model = (
                session.query(self.UserModel)
                .filter(self.UserModel.client_id == client_id.value)
                .filter(self.UserModel.user_id == user_id.value)
                .first()
            )
            if not user_model:
                return Failure(UserNotFoundError(user_id))

            return Success(
                User(
                    name=Name(user_model.name),
                    client_id=ClientId(user_model.client_id),
                    user_id=UserId(user_model.user_id),
                )
            )

    def exists(self, user_id: UserId) -> Result[bool, Error]:
        with self.session_scope() as session:
            user = (
                session.query(self.UserModel)
                .filter(self.UserModel.user_id == user_id.value)
                .first()
            )
            if user:
                return isSuccess
            return Failure(UserNotFoundError(user_id))
