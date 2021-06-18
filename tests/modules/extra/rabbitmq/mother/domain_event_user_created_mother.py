from petisco import DomainEvent, Uuid
from tests.modules.extra.rabbitmq.mother.defaults import DEFAULT_USER_ID


class UserCreated(DomainEvent):
    user_id: Uuid


class DomainEventUserCreatedMother:
    @staticmethod
    def random():
        return UserCreated(user_id=Uuid.v4())

    @staticmethod
    def default():
        return UserCreated(user_id=DEFAULT_USER_ID)

    @staticmethod
    def with_user_id(user_id: Uuid):
        return UserCreated(user_id=user_id)
