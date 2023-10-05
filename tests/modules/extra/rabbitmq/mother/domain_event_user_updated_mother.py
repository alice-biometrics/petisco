from petisco import DomainEvent, Uuid
from tests.modules.extra.rabbitmq.mother.defaults import DEFAULT_USER_ID


class UserUpdated(DomainEvent):
    user_id: Uuid


class DomainEventUserUpdatedMother:
    @staticmethod
    def random() -> UserUpdated:
        return UserUpdated(user_id=Uuid.v4())

    @staticmethod
    def default() -> UserUpdated:
        return UserUpdated(user_id=DEFAULT_USER_ID)

    @staticmethod
    def with_user_id(user_id: Uuid) -> UserUpdated:
        return UserUpdated(user_id=user_id)
