from meiga import isSuccess, BoolResult

from petisco import DomainEvent, MessageSubscriber, Uuid, Message

# Configuration #################################################

ORGANIZATION = "acme"
SERVICE = "registration"
RETRY_TTL = 5000  # default
MAX_RETRIES = 5  # default

# DomainEvent to inform when a user creates an account ##########


class UserCreated(DomainEvent):
    user_id: Uuid

    @staticmethod
    def random():
        return UserCreated(user_id=Uuid.v4())


# Definition of DomainEvent handlers ############################


def send_mail_handler(domain_event: DomainEvent) -> BoolResult:
    print(f"> Send email on {domain_event}")
    return isSuccess  # if fails, returns isFailure


def send_sms_handler(domain_event: DomainEvent) -> BoolResult:
    print(f"> Send sms on {domain_event}")
    return isSuccess  # if fails, returns isFailure


def offer_promotion_handler(domain_event: DomainEvent) -> BoolResult:
    print(f"> Offer promotion on {domain_event}")
    return isSuccess  # if fails, returns isFailure


def message_store(message: Message) -> BoolResult:
    print(f"> Store {message}")
    return isSuccess


# Define subscribers ############################################

sample_user_created_message = UserCreated.random()
subscribers = [
    MessageSubscriber.from_message(
        message=sample_user_created_message,
        handlers=[send_mail_handler, send_sms_handler],
    ),
    MessageSubscriber.from_message(
        message=sample_user_created_message, handlers=[offer_promotion_handler]
    ),
]
