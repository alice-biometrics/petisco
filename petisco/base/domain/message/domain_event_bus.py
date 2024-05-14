from __future__ import annotations

from abc import abstractmethod

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message_bus import MessageBus


class DomainEventBus(MessageBus[DomainEvent]):
    """
    A base class to implement an infrastructure-based bus to publish events.
    """

    @abstractmethod
    def publish(self, domain_event: DomainEvent | list[DomainEvent]) -> None:
        """
        Publish a DomainEvent or a list of DomainEvents
        """
        raise NotImplementedError

    def _check_is_domain_event(self, domain_event: DomainEvent | list[DomainEvent]) -> None:
        if not domain_event or not issubclass(domain_event.__class__, DomainEvent):
            raise TypeError(f"{self.__class__.__name__} only publishes DomainEvent objects")

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
