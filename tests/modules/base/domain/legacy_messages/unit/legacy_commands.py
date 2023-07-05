from __future__ import annotations

from datetime import datetime
from typing import Any

from petisco.base.domain.message.legacy_command import LegacyCommand


class MyCommand(LegacyCommand):
    my_specific_value: str


class NoAttributesCommand(LegacyCommand):
    pass


class AttributesCommand(LegacyCommand):
    id: str
    username: str


class NameConflictCommand(LegacyCommand):
    name: str


class VersionConflictCommand(LegacyCommand):
    version: int

    class Config:
        version = 2


class MostConflictingCommand(LegacyCommand):
    name: str
    version: int
    occurred_on: datetime
    attributes: dict[str, Any]
    meta: dict[str, Any]
    type: str

    class Config:
        version = 2
