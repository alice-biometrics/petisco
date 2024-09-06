from __future__ import annotations

import json

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.domain_event_bus import DomainEventBus


class FileDomainEventBus(DomainEventBus):
    def __init__(self, filename: str):
        self.filename = filename

    def publish(self, domain_event: DomainEvent | list[DomainEvent]) -> None:
        domain_events = [domain_event] if isinstance(domain_event, DomainEvent) else domain_event

        for domain_event in domain_events:
            self._check_is_domain_event(domain_event)

        ordered_domain_events = sorted(domain_events, key=lambda d: d.get_message_occurred_on(), reverse=True)

        serialized_domain_events = {}
        for domain_event in ordered_domain_events:
            message_name = domain_event.get_message_name()
            if message_name not in serialized_domain_events:
                serialized_domain_events[message_name] = [domain_event.format()]
            else:
                serialized_domain_events[message_name].append(domain_event.format())

        with open(self.filename, "w") as json_file:
            json.dump(serialized_domain_events, json_file, indent=4)

    def close(self) -> None:
        pass
