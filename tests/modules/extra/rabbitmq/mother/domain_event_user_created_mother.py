from petisco import DomainEvent, Uuid
from tests.modules.extra.rabbitmq.mother.defaults import DEFAULT_USER_ID


class UserCreated(DomainEvent):
    user_id: Uuid


class DomainEventUserCreatedMother:
    @staticmethod
    def random() -> UserCreated:
        return UserCreated(user_id=Uuid.v4())

    @staticmethod
    def default() -> UserCreated:
        return UserCreated(user_id=DEFAULT_USER_ID)

    @staticmethod
    def with_user_id(user_id: Uuid) -> UserCreated:
        return UserCreated(user_id=user_id)
