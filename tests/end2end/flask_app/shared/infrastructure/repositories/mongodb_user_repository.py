from functools import partial
from typing import Dict

from meiga import Result, Error, isSuccess, Success, Failure

from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from petisco.persistence.pymongo.pymongo_persistence_context import get_mongo_collection
from tests.end2end.flask_app.shared.domain.repositories.interface_user_repository import (
    IUserRepository,
)
from tests.end2end.flask_app.shared.domain.repositories.user_already_exist_error import (
    UserAlreadyExistError,
)
from tests.end2end.flask_app.shared.domain.repositories.user_not_found_error import (
    UserNotFoundError,
)
from tests.end2end.flask_app.user.domain.aggregate_roots.user import User


class MongoDBUserRepository(IUserRepository):
    @staticmethod
    def build():
        return MongoDBUserRepository()

    def __init__(self):
        self.collection_context = partial(get_mongo_collection, "user")

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def save(self, user: User) -> Result[bool, Error]:
        result = self.exists(user.user_id)
        if result.is_success:
            return Failure(UserAlreadyExistError(user.user_id))

        with self.collection_context() as collection:
            if collection.insert_one(user.to_dict()):
                return isSuccess

    def retrieve(self, client_id: ClientId, user_id: UserId) -> Result[User, Error]:
        with self.collection_context() as collection:
            user_doc = collection.find_one(
                {"user_id": user_id.value, "client_id": client_id.value}
            )
            if user_doc:
                return Success(
                    User(
                        name=Name(user_doc.name),
                        client_id=ClientId(user_doc.client_id),
                        user_id=UserId(user_doc.user_id),
                    )
                )
            else:
                return Failure(UserNotFoundError(user_id))

    def exists(self, user_id: UserId) -> Result[bool, Error]:
        with self.collection_context() as collection:
            if collection.find_one({"user_id": user_id.value}):
                return isSuccess
            else:
                return Failure(UserNotFoundError(user_id))
