from abc import ABC
from typing import List

from pydantic.main import BaseModel

from petisco.base.domain.model.uuid import Uuid
from petisco.base.domain.message.domain_event import DomainEvent


class AggregateRoot(ABC, BaseModel):
    aggregate_id: Uuid
    aggregate_version: int = 1
    _domain_events = []

    def record(self, domain_event: DomainEvent):
        self._domain_events.append(domain_event)

    def clear_domain_events(self):
        self._domain_events = []

    def pull_domain_events(self) -> List[DomainEvent]:
        return self._domain_events

    def pull_first_domain_event(self) -> DomainEvent:
        return self._domain_events[0] if len(self._domain_events) > 0 else None

    def pull_last_domain_event(self) -> DomainEvent:
        return self._domain_events[-1] if len(self._domain_events) > 0 else None
