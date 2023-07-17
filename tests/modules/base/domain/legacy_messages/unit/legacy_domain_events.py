from __future__ import annotations

from datetime import datetime
from typing import Any

from petisco.base.domain.message.legacy.legacy_domain_event import LegacyDomainEvent


class MyDomainEvent(LegacyDomainEvent):
    my_specific_value: str


class NoAttributesDomainEvent(LegacyDomainEvent):
    pass


class AttributesDomainEvent(LegacyDomainEvent):
    id: str
    username: str


class NameConflictDomainEvent(LegacyDomainEvent):
    name: str


class VersionConflictDomainEvent(LegacyDomainEvent):
    version: int

    class Config:
        version = 2


class MostConflictingDomainEvent(LegacyDomainEvent):
    name: str
    version: int
    occurred_on: datetime
    attributes: dict[str, Any]
    meta: dict[str, Any]
    type: str

    class Config:
        version = 2
