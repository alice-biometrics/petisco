from typing import List, Type

from meiga import isSuccess, BoolResult

from petisco import (
    DomainEvent,
    Uuid,
    Message,
    DomainEventSubscriber,
    AllMessageSubscriber,
    CommandSubscriber,
    Command,
)

# Configuration #################################################

ORGANIZATION = "acme"
SERVICE = "registration"
RETRY_TTL = 5000  # default
MAX_RETRIES = 5  # default

# DomainEvents and Commands


class UserCreated(DomainEvent):
    user_id: Uuid


class UserConfirmed(DomainEvent):
    user_id: Uuid


class UserPersisted(DomainEvent):
    user_id: Uuid


class PersistUser(Command):
    user_id: Uuid


# Domain Events Subscribers


class SendMailOnUserCreated(DomainEventSubscriber):
    def subscribed_to(self) -> List[Type[DomainEvent]]:
        return [UserCreated]

    def handle(self, domain_event: DomainEvent) -> BoolResult:
        print(f"> Send email on {domain_event.dict()}\n")
        return isSuccess  # if fails, returns isFailure


class SendSmsOnUserConfirmed(DomainEventSubscriber):
    def subscribed_to(self) -> List[Type[DomainEvent]]:
        return [UserConfirmed]

    def handle(self, domain_event: DomainEvent) -> BoolResult:
        print(f"> Send sms on {domain_event.dict()}\n")
        return isSuccess  # if fails, returns isFailure


class StoreOnMessage(AllMessageSubscriber):
    def handle(self, message: Message) -> BoolResult:
        print(f"> Store {message.dict()}\n")
        return isSuccess  # if fails, returns isFailure


# Command Subscribers (or Command Handlers)


class PersistUserHandler(CommandSubscriber):
    def subscribed_to(self) -> Type[Command]:
        return PersistUser

    def handle(self, command: PersistUser) -> BoolResult:
        print(f"> PersistUser on {command.dict()}\n")
        # self.domain_event_bus.publish(UserPersisted(user_id=command.user_id))
        return isSuccess  # if fails, returns isFailure


subscribers = [
    SendMailOnUserCreated,
    StoreOnMessage,
    SendSmsOnUserConfirmed,
    PersistUserHandler,
]
