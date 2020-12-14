from petisco import Event, UserId
from tests.modules.event.mothers.defaults import DEFAULT_USER_ID


class UserUpdated(Event):
    user_id: UserId

    def __init__(self, user_id: UserId):
        self.user_id = user_id
        super().__init__()


class EventUserUpdatedMother:
    @staticmethod
    def random():
        return UserUpdated(user_id=UserId.generate())

    @staticmethod
    def default():
        return UserUpdated(user_id=DEFAULT_USER_ID)

    @staticmethod
    def with_user_id(user_id: UserId):
        return UserUpdated(user_id=user_id)
