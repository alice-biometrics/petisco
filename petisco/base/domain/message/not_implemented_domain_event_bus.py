from __future__ import annotations

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus


class NotImplementedDomainEventBus(DomainEventBus):
    def publish(self, domain_event: DomainEvent | list[DomainEvent]) -> None:
        domain_events = [domain_event] if isinstance(domain_event, DomainEvent) else domain_event
        for domain_event in domain_events:
            self._check_is_domain_event(domain_event)
            meta = self.get_configured_meta()
            _ = domain_event.update_meta(meta)

    def retry_publish(
        self,
        domain_event: DomainEvent,
        retry_routing_key: str,
        retry_exchange_name: str | None = None,
    ) -> None:
        self._check_is_domain_event(domain_event)
        meta = self.get_configured_meta()
        _ = domain_event.update_meta(meta)

    def close(self) -> None:
        pass
