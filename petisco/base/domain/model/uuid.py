import os
from typing import Any
from uuid import uuid4

import validators
from pydantic import UUID4, GetCoreSchemaHandler
from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    no_info_after_validator_function,
    plain_serializer_function_ser_schema,
    uuid_schema,
)

from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid

USE_LEGACY_UUID = bool(os.getenv("USE_LEGACY_UUID", "False").lower() == "true")


class Uuid(str):
    """
    A base class to define Uuid

    Use it to identify domain entities
    """

    def __new__(cls, value: str) -> "Uuid":
        if value is None or not validators.uuid(value):
            raise InvalidUuid(uuid_value=value)
        return str.__new__(cls, value)

    def __repr__(self) -> str:
        return self

    # def __init__(self, value: str) -> None:
    #     if value is None or not validators.uuid(value):
    #         raise InvalidUuid(uuid_value=value)
    #     #super().__init__(str(value))
    #     self._value = value

    @classmethod
    def v4(cls) -> "Uuid":
        return cls(value=str(uuid4()))

    def to_str(self) -> str:
        return self

    @staticmethod
    def from_str(value: str) -> "Uuid":
        return Uuid(value)

    @property
    def value(self) -> str:
        return self.to_str()

    @classmethod
    def from_value(cls, value: str) -> "Uuid":
        return cls(value)

    # @classmethod
    # def __get_pydantic_core_schema__(
    #     cls, source: Any, handler: GetCoreSchemaHandler
    # ) -> CoreSchema:
    #     return uuid_schema(version=4)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        # assert source is Uuid
        return no_info_after_validator_function(
            cls._validate,
            uuid_schema(version=4, strict=False),
            serialization=plain_serializer_function_ser_schema(
                cls._serialize,
                info_arg=False,
                return_schema=uuid_schema(version=4, strict=False),
            ),
        )

    @staticmethod
    def _validate(value: UUID4) -> "Uuid":
        return Uuid(str(value))
        # if isinstance(value, str):
        #     return Uuid(value
        #                 )
        # if isinstance(value, dict):
        #     return Uuid(value["value"])
        # else:
        #     return Uuid(value.value)

    @staticmethod
    def _serialize(value: "Uuid") -> str:
        return value.value


if USE_LEGACY_UUID:
    from petisco.base.domain.model.legacy_uuid import LegacyUuid  # noqa

    Uuid = LegacyUuid  # noqa
