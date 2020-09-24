from meiga import Result, Error, isSuccess

from petisco import Event, UserId, EventSubscriber

# Configuration
ORGANIZATION = "alice"
SERVICE = "petisco"
RETRY_TTL = 5000  # default
MAX_RETRIES = 5  # default


class UserCreated(Event):
    user_id: UserId

    def __init__(self, user_id: UserId):
        self.user_id = user_id
        super().__init__()

    @staticmethod
    def random():
        return UserCreated(UserId.generate())


def send_mail_handler(event: Event) -> Result[bool, Error]:
    print(f"Send email on {event}")
    return isSuccess  # if fails, returns isFailure


event = UserCreated.random()

subscribers = [EventSubscriber(event, [send_mail_handler])]
