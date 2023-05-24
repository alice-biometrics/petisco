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
