from meiga import isSuccess, BoolResult

from petisco import Event, UserId, EventSubscriber

# Configuration
ORGANIZATION = "acme"
SERVICE = "legacy"
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


def send_mail_handler(event: Event) -> BoolResult:
    print(f"> Send email on {event}")
    return isSuccess  # if fails, returns isFailure


def send_sms_handler(event: Event) -> BoolResult:
    print(f"> Send sms on {event}")
    return isSuccess  # if fails, returns isFailure


def offer_promotion_handler(event: Event) -> BoolResult:
    print(f"> Offer promotion on {event}")
    return isSuccess  # if fails, returns isFailure


def event_store(event: Event) -> BoolResult:
    print(f"> Store {event}")
    return isSuccess


subscribers = [
    EventSubscriber(
        event_name="UserCreated",
        event_version=1,
        handlers=[send_mail_handler, send_sms_handler],
    ),
    EventSubscriber(
        event_name="UserCreated", event_version=1, handlers=[offer_promotion_handler]
    ),
]
