from typing import Union

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus


class NotImplementedDomainEventBus(DomainEventBus):
    def publish(self, domain_event: DomainEvent) -> None:
        self._check_is_domain_event(domain_event)
        meta = self.get_configured_meta()
        _ = domain_event.update_meta(meta)

    def retry_publish_only_on_store_queue(self, domain_event: DomainEvent) -> None:
        self._check_is_domain_event(domain_event)
        meta = self.get_configured_meta()
        _ = domain_event.update_meta(meta)

    def retry_publish(
        self,
        domain_event: DomainEvent,
        retry_routing_key: str,
        retry_exchange_name: Union[str, None] = None,
    ) -> None:
        self._check_is_domain_event(domain_event)
        meta = self.get_configured_meta()
        _ = domain_event.update_meta(meta)

    def close(self) -> None:
        pass
