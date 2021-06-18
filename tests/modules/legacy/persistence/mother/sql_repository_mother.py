import os
from typing import List

from attr import dataclass
from meiga import BoolResult, Result, Error, isSuccess, Success

from petisco.legacy import Persistence, SqlRepository, UserId, ClientId

BASE_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/../ymls/"


@dataclass
class User:
    user_id: UserId
    name: str

    @staticmethod
    def random():
        return User(UserId.generate(), "MyName")

    def to_dict(self):
        return {"user_id": self.user_id.value, "name": self.name}

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(
            self.__class__, other.__class__
        ):
            return self.to_dict() == other.to_dict()
        else:
            return False

    @staticmethod
    def from_dict(kdict: dict):
        return User(UserId(kdict.get("user_id")), kdict.get("name"))


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


class MyUserSqlRepository(SqlRepository):
    def __init__(self, database_name: str):
        self.session_scope = Persistence.get_session_scope(database_name)
        self.UserModel = Persistence.get_model(database_name, "user")
        self.ClientModel = Persistence.get_model(database_name, "client")

    def save(self, user: User) -> BoolResult:
        with self.session_scope() as session:
            client_internal_id = self.get_sql_internal_client_id(
                session, self.ClientModel
            ).unwrap_or_return()
            user_model = (
                session.query(self.UserModel)
                .filter(self.UserModel.user_id == user.user_id.value)
                .filter(self.UserModel.client_id == client_internal_id)
                .first()
            )
            self.fail_if_entity_already_exist(
                user_model, user.user_id
            ).unwrap_or_return()
            user_model = self.UserModel(**user.to_dict())
            user_model.client_id = client_internal_id
            session.add(user_model)
        return isSuccess

    def retrieve(self, user_id: UserId) -> Result[User, Error]:
        with self.session_scope() as session:
            client_internal_id = self.get_sql_internal_client_id(
                session, self.ClientModel
            ).unwrap_or_return()
            user_model = (
                session.query(self.UserModel)
                .filter(self.UserModel.user_id == user_id.value)
                .filter(self.UserModel.client_id == client_internal_id)
                .first()
            )
            self.fail_if_entity_not_exist(user_model, user_id).unwrap_or_return()
            user = User.from_dict(user_model.__dict__)
            return Success(user)

    def retrieve_all(self) -> Result[List[User], Error]:
        with self.session_scope() as session:
            client_internal_id = self.get_sql_internal_client_id(
                session, self.ClientModel
            ).unwrap_or_return()
            user_models = (
                session.query(self.UserModel)
                .filter(self.UserModel.client_id == client_internal_id)
                .all()
            )
            self.fail_if_entities_not_exist(user_models).unwrap_or_return()
            users = [User.from_dict(user_model.__dict__) for user_model in user_models]
            return Success(users)

    def remove(self, Any) -> BoolResult:
        pass


class MyClientSqlRepository(SqlRepository):
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
            self.fail_if_entity_not_exist(client_model, client_id).unwrap_or_return()
            client = Client.from_dict(client_model.__dict__)
            return Success(client)

    def retrieve_all(self, Any) -> Result[List[User], Error]:
        pass

    def remove(self, Any) -> BoolResult:
        pass


class SqlRepositoryMother:
    @staticmethod
    def user(database_name: str):
        MyClientSqlRepository(database_name).save(Client.random())
        return MyUserSqlRepository(database_name).with_client_id(ClientId("ACME"))
