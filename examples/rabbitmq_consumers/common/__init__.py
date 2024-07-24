import random
from time import sleep
from typing import List, Type

from meiga import BoolResult, isSuccess

from petisco import (
    DomainEvent,
    DomainEventSubscriber,
    Uuid,
)

# Configuration #################################################

ORGANIZATION = "acme"
SERVICE = "registration"
RETRY_TTL = 5000  # default
MAX_RETRIES = 5  # default


class UserCreated(DomainEvent):
    user_id: Uuid


def wait() -> None:
    seconds = random.uniform(0, 1)
    print(f"waiting {seconds:0.2f} s...")
    sleep(seconds)


class ProcessOnUserCreated(DomainEventSubscriber):
    def __init__(self) -> None:
        self.counter = 0

    def subscribed_to(self) -> List[Type[DomainEvent]]:
        return [UserCreated]

    def handle(self, domain_event: DomainEvent) -> BoolResult:
        print(f"> Processed on {domain_event.format()}\n")
        wait()
        self.counter += 1
        print(f"Processed {self.counter} domain events")
        return isSuccess  # if fails, returns isFailure


subscribers = [ProcessOnUserCreated]
