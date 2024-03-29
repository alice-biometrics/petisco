from petisco import Command, Uuid
from tests.modules.extra.rabbitmq.mother.defaults import DEFAULT_USER_ID


class PersistUser(Command):
    user_id: Uuid


class CommandPersistUserMother:
    @staticmethod
    def random() -> PersistUser:
        return PersistUser(user_id=Uuid.v4())

    @staticmethod
    def default() -> PersistUser:
        return PersistUser(user_id=DEFAULT_USER_ID)

    @staticmethod
    def with_user_id(user_id: Uuid) -> PersistUser:
        return PersistUser(user_id=user_id)
