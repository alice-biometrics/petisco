import os
from typing import List

from attr import dataclass
from meiga import BoolResult, Error, Result, Success, isSuccess
from meiga.decorators import meiga

from petisco import Uuid, ValueObject
from petisco.extra.sqlalchemy.sql.sql_repository import SqlRepository
from tests.modules.extra.sqlalchemy.mother.models import ClientModel, UserModel

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
        if issubclass(other.__class__, self.__class__) or issubclass(self.__class__, other.__class__):
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
        return Client(ClientId(value="ACME"), "ACME")

    def to_dict(self):
        return {"client_id": self.client_id.value, "name": self.name}

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__) or issubclass(self.__class__, other.__class__):
            return self.to_dict() == other.to_dict()
        else:
            return False

    @staticmethod
    def from_dict(kdict: dict):
        return Client(ClientId(kdict.get("client_id")), kdict.get("name"))


class MyUserSqlRepository(SqlRepository):
    @meiga
    def save(self, user: User) -> BoolResult:
        with self.session_scope() as session:
            client_model = (
                session.query(ClientModel).filter(ClientModel.client_id == user.client_id.value).first()
            )
            self.fail_if_aggregate_not_found(client_model, user.client_id).unwrap_or_return()

            user_model = (
                session.query(UserModel)
                .filter(UserModel.user_id == user.user_id.value)
                .filter(UserModel.client_id == client_model.client_id)
                .first()
            )
            self.fail_if_aggregate_already_exist(user_model, user.user_id).unwrap_or_return()
            user_model = UserModel(**user.to_dict())
            session.add(user_model)
        return isSuccess

    @meiga
    def retrieve(self, user_id: UserId) -> Result[User, Error]:
        with self.session_scope() as session:
            user_model = session.query(UserModel).filter(UserModel.user_id == user_id.value).first()
            self.fail_if_aggregate_not_found(user_model, user_id).unwrap_or_return()
            user = User.from_dict(user_model.__dict__)
            return Success(user)

    @meiga
    def retrieve_all(self, client_id: ClientId) -> Result[List[User], Error]:
        with self.session_scope() as session:
            client_model = session.query(ClientModel).filter(ClientModel.client_id == client_id.value).first()
            self.fail_if_aggregate_not_found(client_model, client_id).unwrap_or_return()

            user_models = session.query(UserModel).filter(UserModel.client_id == client_model.id).all()
            self.fail_if_aggregates_not_found(user_models).unwrap_or_return()
            users = [User.from_dict(user_model.__dict__) for user_model in user_models]
            return Success(users)


class MyClientSqlRepository(SqlRepository):
    @meiga
    def save(self, client: Client) -> BoolResult:
        with self.session_scope() as session:
            client_model = (
                session.query(ClientModel).filter(ClientModel.client_id == client.client_id.value).first()
            )
            self.fail_if_aggregate_already_exist(client_model, client.client_id).unwrap_or_return()
            client_model = ClientModel(**client.to_dict())
            session.add(client_model)
        return isSuccess

    @meiga
    def retrieve(self, client_id: ClientId) -> Result[Client, Error]:
        with self.session_scope() as session:
            client_model = session.query(ClientModel).filter(ClientModel.client_id == client_id.value).first()
            self.fail_if_aggregate_not_found(client_model, client_id).unwrap_or_return()
            client = Client.from_dict(client_model.__dict__)
            return Success(client)


class SqlRepositoryMother:
    @staticmethod
    def with_client(client: Client = Client.random()):
        MyClientSqlRepository().save(client)
        return MyUserSqlRepository()

    @staticmethod
    def with_user(
        user: User,
        client: Client = Client.random(),
    ):
        MyClientSqlRepository().save(client)
        user_repository = MyUserSqlRepository()
        user_repository.save(user)
        return user_repository
