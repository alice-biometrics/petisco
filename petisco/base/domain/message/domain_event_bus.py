from abc import abstractmethod
from typing import Union

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message_bus import MessageBus


class DomainEventBus(MessageBus[DomainEvent]):
    """
    A base class to implement an infrastructure-based bus to publish events.
    """

    @abstractmethod
    def publish(self, domain_event: DomainEvent) -> None:
        """
        Publish one DomainEvent
        """
        raise NotImplementedError

    @abstractmethod
    def retry_publish_only_on_store_queue(self, domain_event: DomainEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def retry_publish(
        self,
        domain_event: DomainEvent,
        retry_routing_key: str,
        retry_exchange_name: Union[str, None] = None,
    ) -> None:
        raise NotImplementedError

    def _check_is_domain_event(self, domain_event: DomainEvent) -> None:
        if not domain_event or not issubclass(domain_event.__class__, DomainEvent):
            raise TypeError("DomainEventBus only publishes DomainEvent objects")

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
