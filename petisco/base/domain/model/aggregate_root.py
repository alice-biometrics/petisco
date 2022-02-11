from abc import ABC
from typing import List

from pydantic import BaseModel, NonNegativeInt, PrivateAttr, validator

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.model.uuid import Uuid

DEFAULT_VERSION = 1


class AggregateRoot(ABC, BaseModel):
    aggregate_id: Uuid = None
    aggregate_version: NonNegativeInt = None
    _domain_events = PrivateAttr(default=[])

    @validator("aggregate_id", pre=True, always=True)
    def set_aggregate_id(cls, v):
        v = Uuid(v) if isinstance(v, str) else v
        return v or Uuid.v4()

    @validator("aggregate_version", pre=True, always=True)
    def set_aggregate_version(cls, v):
        return v or DEFAULT_VERSION

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
