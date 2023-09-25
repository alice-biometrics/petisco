import os
from typing import Any
from uuid import uuid4

import validators
from pydantic import UUID4, GetCoreSchemaHandler
from pydantic_core import CoreSchema
from pydantic_core.core_schema import uuid_schema

from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid

USE_LEGACY_UUID = bool(os.getenv("USE_LEGACY_UUID", "False").lower() == "true")


class Uuid(UUID4):
    """
    A base class to define Uuid

    Use it to identify domain entities
    """

    def __init__(self, value: str) -> None:
        if value is None or not validators.uuid(value):
            raise InvalidUuid(uuid_value=value)
        super().__init__(str(value))

    @classmethod
    def v4(cls) -> "Uuid":
        return cls(value=uuid4())

    def to_str(self) -> str:
        return str(self)

    @staticmethod
    def from_str(value: str) -> "Uuid":
        return Uuid(value)

    @property
    def value(self) -> str:
        return self.to_str()

    @classmethod
    def from_value(cls, value: str) -> "Uuid":
        return cls(value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return uuid_schema(version=4)


# if USE_LEGACY_UUID:
#     from petisco.base.domain.model.legacy_uuid import LegacyUuid #noqa
#     Uuid = LegacyUuid # noqa
