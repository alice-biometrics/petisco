from typing import Dict

from meiga import Result, Error, isSuccess, Success, Failure

from petisco.application.repository import Repository
from petisco.domain.entities.client_id import ClientId
from petisco.domain.entities.name import Name
from petisco.domain.entities.user_id import UserId
from petisco.persistence.sqlalchemy.sqlalchemy_session_scope import session_scope
from tests.integration.controller.toy_app.domain.repositories.user_already_exist_error import (
    UserAlreadyExistError,
)
from tests.integration.controller.toy_app.domain.repositories.user_not_found_error import (
    UserNotFoundError,
)
from tests.integration.controller.toy_app.infrastructure.repositories.user_model import (
    UserModel,
)


class SqlUserRepository(Repository):
    def __init__(self):
        self.users = {}

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def save(
        self, client_id: ClientId, user_id: UserId, name: Name
    ) -> Result[bool, Error]:
        result = self.exists(user_id)
        if result.is_success:
            return Failure(UserAlreadyExistError(user_id))

        with session_scope() as session:
            user = UserModel(client_id=client_id, user_id=user_id, name=name)
            session.add(user)
        return isSuccess

    def find_name(self, client_id: ClientId, user_id: UserId) -> Result[Name, Error]:
        with session_scope() as session:
            user_model = (
                session.query(UserModel)
                .filter(UserModel.client_id == client_id)
                .filter(UserModel.user_id == user_id)
                .first()
            )
            if not user_model:
                return Failure(UserNotFoundError(user_id))

            return Success(Name(user_model.name))

    def exists(self, user_id: str) -> Result[bool, Error]:
        with session_scope() as session:
            user = session.query(UserModel).filter(UserModel.user_id == user_id).first()
            if user:
                return isSuccess
            return Failure(UserNotFoundError(user_id))
