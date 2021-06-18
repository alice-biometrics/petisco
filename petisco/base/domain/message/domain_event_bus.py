from abc import abstractmethod

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message_bus import MessageBus


class DomainEventBus(MessageBus):
    @abstractmethod
    def publish(self, domain_event: DomainEvent):
        raise NotImplementedError

    @abstractmethod
    def retry_publish_only_on_store_queue(self, domain_event: DomainEvent):
        raise NotImplementedError

    def _check_is_domain_event(self, domain_event: DomainEvent):
        if not domain_event or not issubclass(domain_event.__class__, DomainEvent):
            raise TypeError("DomainEventBus only publishes DomainEvent objects")

    @abstractmethod
    def close(self):
        raise NotImplementedError
