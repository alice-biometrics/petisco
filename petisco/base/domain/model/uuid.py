import os
from typing import Any
from uuid import UUID, uuid4

import validators
from pydantic import field_validator

from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid
from petisco.base.domain.model.value_object import ValueObject

USE_NEW_UUID = bool(os.getenv("USE_NEW_UUID", "False").lower() == "true")

if USE_NEW_UUID:
    from pydantic import GetCoreSchemaHandler  # noqa
    from pydantic_core import CoreSchema  # noqa
    from pydantic_core.core_schema import uuid_schema  # noqa

    class Uuid(UUID):
        """
        A base class to define Uuid

        Use it to identify domain entities
        """

        def __init__(self, value: str) -> None:
            if value is None or not validators.uuid(value):
                raise InvalidUuid(uuid_value=value)
            super().__init__(value)

        @classmethod
        def v4(cls) -> "Uuid":
            return cls(str(uuid4()))

        def to_str(self) -> str:
            return str(self)

        @staticmethod
        def from_str(value: str) -> "Uuid":
            return Uuid(value)

        @property
        def value(self) -> str:
            return self.to_str()

        @classmethod
        def from_value(cls, value: Any) -> "Uuid":
            return cls(value=str(value))

        @classmethod
        def __get_pydantic_core_schema__(
            cls, source: Any, handler: GetCoreSchemaHandler
        ) -> CoreSchema:
            return uuid_schema(version=4)

else:

    class Uuid(ValueObject):
        """
        A base class to define Uuid

        Use it to identify domain entities
        """

        value: str

        @field_validator("value")
        def validate_value(cls, value: str) -> str:
            if value is None or not validators.uuid(value):
                raise InvalidUuid(uuid_value=value)
            return value

        @classmethod
        def v4(cls) -> "Uuid":
            return cls(value=str(uuid4()))

        def to_uuid(self) -> UUID:
            return UUID(self.value)

        def to_str(self) -> str:
            return str(self.value)

        @staticmethod
        def from_uuid(uuid: UUID) -> "Uuid":
            return Uuid(value=str(uuid))

        @staticmethod
        def from_str(value: str) -> "Uuid":
            return Uuid(value=value)
