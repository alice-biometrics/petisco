import sys
from uuid import uuid4

import validators
from pydantic import validator

from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid
from petisco.base.domain.model.value_object import ValueObject

if sys.version_info < (3, 11):
    Self = "Uuid"
else:
    from typing import Self  # noqa


class Uuid(ValueObject):
    """
    A base class to define Uuid

    Use it to identify domain entities
    """

    value: str

    @validator("value")
    def validate_value(cls, value: str) -> str:
        if value is None or not validators.uuid(value):
            raise InvalidUuid(uuid_value=value)
        return value

    @classmethod
    def v4(cls) -> Self:
        return cls(value=str(uuid4()))
