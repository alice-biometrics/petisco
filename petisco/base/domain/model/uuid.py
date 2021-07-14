from uuid import uuid4

import validators
from pydantic import validator

from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid
from petisco.base.domain.model.value_object import ValueObject


class Uuid(ValueObject):
    @validator("value")
    def validate_value(cls, value):
        if value is None or not validators.uuid(value):
            raise InvalidUuid(uuid_value=value)
        return value

    @staticmethod
    def v4():
        return Uuid(value=str(uuid4()))
