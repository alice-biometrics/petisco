from uuid import UUID, uuid4

import validators
from pydantic import field_validator

from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid
from petisco.base.domain.model.value_object import ValueObject


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
