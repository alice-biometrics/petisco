from __future__ import annotations

from abc import abstractmethod

from meiga import BoolResult

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message_subscriber import MessageSubscriber


class DomainEventSubscriber(MessageSubscriber):
    """
    A base class to model your events subscribers.
    Inherit from this class to parser the domain event, configure middlewares and instantiate and execute a UseCase.
    """

    @abstractmethod
    def subscribed_to(self) -> list[type[DomainEvent]]:
        """
        returns the list of events that we want to subscribe
        """
        raise NotImplementedError()

    @abstractmethod
    def handle(self, domain_event: DomainEvent) -> BoolResult:
        """
        returns True if the event was processed or False if it could not be processed
        """
        raise NotImplementedError()
