from abc import ABC
from copy import copy
from typing import List, Union

from pydantic import BaseModel, Field, NonNegativeInt, PrivateAttr, validator

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.model.uuid import Uuid

DEFAULT_VERSION = 1


class AggregateRoot(ABC, BaseModel):
    """
    A base class to define AggregateRoot

    It is a cluster of associated entities that are treated as a unit for the purpose of data changes.
    """

    aggregate_id: Uuid = Field(default=Uuid.v4())
    aggregate_version: NonNegativeInt = Field(default=DEFAULT_VERSION)
    _domain_events: List[DomainEvent] = PrivateAttr(default=[])

    @validator("aggregate_id", pre=True, always=True)
    def set_aggregate_id(cls, v: Union[str, Uuid]) -> Uuid:
        v = Uuid(v) if isinstance(v, str) else v
        return v or Uuid.v4()

    @validator("aggregate_version", pre=True, always=True)
    def set_aggregate_version(cls, v: NonNegativeInt) -> NonNegativeInt:
        return v or DEFAULT_VERSION

    def record(self, domain_event: DomainEvent) -> None:
        """
        Record something that happened is our domain related with the aggregate (a DomainEvent).
        """
        self._domain_events.append(domain_event)

    def clear_domain_events(self) -> None:
        """
        Clear all domain events recorded.
        """
        self._domain_events = []

    def pull_domain_events(self) -> List[DomainEvent]:
        """
        Returns and clear all domain events recorded.
        """
        domain_events = copy(self._domain_events)
        self.clear_domain_events()
        return domain_events

    def get_domain_events(self) -> List[DomainEvent]:
        """
        Returns all domain events recorded.
        """
        return self._domain_events

    def get_first_domain_event(self) -> Union[DomainEvent, None]:
        """
        Returns only the first domain event recorded.
        """
        return self._domain_events[0] if len(self._domain_events) > 0 else None

    def get_last_domain_event(self) -> Union[DomainEvent, None]:
        """
        Returns only the last domain event recorded.
        """
        return self._domain_events[-1] if len(self._domain_events) > 0 else None
