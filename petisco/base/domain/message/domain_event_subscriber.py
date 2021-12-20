from abc import abstractmethod
from typing import List, Type

from meiga import BoolResult

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message_subscriber import MessageSubscriber


class DomainEventSubscriber(MessageSubscriber):
    @abstractmethod
    def subscribed_to(self) -> List[Type[DomainEvent]]:
        raise NotImplementedError()

    @abstractmethod
    def handle(self, domain_event: DomainEvent) -> BoolResult:
        raise NotImplementedError()
