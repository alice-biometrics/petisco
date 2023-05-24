from datetime import datetime
from typing import Any

from petisco import Command


class MyCommand(Command):
    my_specific_value: str


class NoAttributesCommand(Command):
    pass


class AttributesCommand(Command):
    id: str
    username: str


class NameConflictCommand(Command):
    name: str


class VersionConflictCommand(Command):
    version: int

    class Config:
        version = 2


class MostConflictingCommand(Command):
    name: str
    version: int
    occurred_on: datetime
    attributes: dict[str, Any]
    meta: dict[str, Any]
    type: str

    class Config:
        version = 2
