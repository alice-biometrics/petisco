from datetime import datetime
from typing import Any, Dict

from petisco import DomainEvent


class MyDomainEvent(DomainEvent):
    my_specific_value: str


class NoAttributesDomainEvent(DomainEvent):
    pass


class AttributesDomainEvent(DomainEvent):
    id: str
    username: str


class NameConflictDomainEvent(DomainEvent):
    name: str


class VersionConflictDomainEvent(DomainEvent):
    version: int

    class Config:
        version = 2


class MostConflictingDomainEvent(DomainEvent):
    name: str
    version: int
    occurred_on: datetime
    attributes: Dict[str, Any]
    meta: Dict[str, Any]
    type: str

    class Config:
        version = 2
