from petisco import DomainEvent, Uuid, ValueObject
from tests.modules.extra.rabbitmq.mother.defaults import DEFAULT_USER_ID


class UserCreated(DomainEvent):
    user_id: Uuid

    _user_id = ValueObject.serializer("user_id")


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
