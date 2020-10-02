from petisco import Event, UserId
from tests.modules.event.mothers.defaults import DEFAULT_USER_ID


class UserCreated(Event):
    user_id: UserId

    def __init__(self, user_id: UserId):
        self.user_id = user_id
        super().__init__()


class EventUserCreatedMother:
    @staticmethod
    def random():
        return UserCreated(user_id=UserId.generate())

    @staticmethod
    def default():
        return UserCreated(user_id=DEFAULT_USER_ID)

    @staticmethod
    def with_user_id(user_id: UserId):
        return UserCreated(user_id=user_id)
