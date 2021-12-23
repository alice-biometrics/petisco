import os
from typing import List

from attr import dataclass
from meiga import BoolResult, Error, Result, Success, isSuccess

from petisco import Uuid, ValueObject
from petisco.base.domain.persistence.persistence import Persistence
from petisco.extra.sqlalchemy.sql.base_sql_repository import BaseSqlRepository

BASE_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../ymls/"


class UserId(Uuid):
    pass


class ClientId(ValueObject):
    pass


@dataclass
class User:
    user_id: UserId
    name: str
    client_id: ClientId

    @staticmethod
    def random():
        return User(UserId.v4(), "MyName", ClientId("Client1"))

    def to_dict(self):
        return {
            "user_id": self.user_id.value,
            "name": self.name,
            "client_id": self.client_id.value,
        }

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(
            self.__class__, other.__class__
        ):
            return self.to_dict() == other.to_dict()
        else:
            return False

    @staticmethod
    def from_dict(kdict: dict):
        return User(
            UserId(kdict.get("user_id")),
            kdict.get("name"),
            ClientId(kdict.get("client_id")),
        )


@dataclass
class Client:
    client_id: ClientId
    name: str

    @staticmethod
    def random():
        return Client(ClientId("ACME"), "ACME")

    def to_dict(self):
        return {"client_id": self.client_id.value, "name": self.name}

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(
            self.__class__, other.__class__
        ):
            return self.to_dict() == other.to_dict()
        else:
            return False

    @staticmethod
    def from_dict(kdict: dict):
        return Client(ClientId(kdict.get("client_id")), kdict.get("name"))


class MyUserSqlRepository(BaseSqlRepository):
    def __init__(self, database_name: str):
        self.session_scope = Persistence.get_session_scope(database_name)
        self.UserModel = Persistence.get_model(database_name, "user")
        self.ClientModel = Persistence.get_model(database_name, "client")

    def save(self, user: User) -> BoolResult:
        with self.session_scope() as session:
            client_model = (
                session.query(self.ClientModel)
                .filter(self.ClientModel.client_id == user.client_id.value)
                .first()
            )
            self.fail_if_entity_not_found(
                client_model, user.client_id
            ).unwrap_or_return()

            user_model = (
                session.query(self.UserModel)
                .filter(self.UserModel.user_id == user.user_id.value)
                .filter(self.UserModel.client_id == client_model.id)
                .first()
            )
            self.fail_if_entity_already_exist(
                user_model, user.user_id
            ).unwrap_or_return()
            user_model = self.UserModel(**user.to_dict())
            session.add(user_model)
        return isSuccess

    def retrieve(self, user_id: UserId) -> Result[User, Error]:
        with self.session_scope() as session:
            user_model = (
                session.query(self.UserModel)
                .filter(self.UserModel.user_id == user_id.value)
                .first()
            )
            self.fail_if_entity_not_found(user_model, user_id).unwrap_or_return()
            user = User.from_dict(user_model.__dict__)
            return Success(user)

    def retrieve_all(self, client_id: ClientId) -> Result[List[User], Error]:
        with self.session_scope() as session:
            client_model = (
                session.query(self.ClientModel)
                .filter(self.ClientModel.client_id == client_id.value)
                .first()
            )
            self.fail_if_entity_not_found(client_model, client_id).unwrap_or_return()

            user_models = (
                session.query(self.UserModel)
                .filter(self.UserModel.client_id == client_model.id)
                .all()
            )
            self.fail_if_entities_not_found(user_models).unwrap_or_return()
            users = [User.from_dict(user_model.__dict__) for user_model in user_models]
            return Success(users)


class MyClientSqlRepository(BaseSqlRepository):
    def __init__(self, database_name: str):
        self.session_scope = Persistence.get_session_scope(database_name)
        self.ClientModel = Persistence.get_model(database_name, "client")

    def save(self, client: Client) -> BoolResult:
        with self.session_scope() as session:
            client_model = (
                session.query(self.ClientModel)
                .filter(self.ClientModel.client_id == client.client_id.value)
                .first()
            )
            self.fail_if_entity_already_exist(
                client_model, client.client_id
            ).unwrap_or_return()
            client_model = self.ClientModel(**client.to_dict())
            session.add(client_model)
        return isSuccess

    def retrieve(self, client_id: ClientId) -> Result[Client, Error]:
        with self.session_scope() as session:
            client_model = (
                session.query(self.ClientModel)
                .filter(self.ClientModel.client_id == client_id.value)
                .first()
            )
            self.fail_if_entity_not_found(client_model, client_id).unwrap_or_return()
            client = Client.from_dict(client_model.__dict__)
            return Success(client)


class SqlRepositoryMother:
    @staticmethod
    def with_client(
        database_name: str = "sqlite_test", client: Client = Client.random()
    ):
        MyClientSqlRepository(database_name).save(client)
        return MyUserSqlRepository(database_name)
