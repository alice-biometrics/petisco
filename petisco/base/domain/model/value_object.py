from typing import Any

from pydantic import validator
from pydantic.main import BaseModel

from petisco.base.domain.errors.defaults.invalid_value_object import InvalidValueObject


class ValueObject(BaseModel):
    value: Any

    def __init__(self, value: Any, **data) -> None:
        super().__init__(value=value, **data)

    def dict(self, **kwargs):
        return self.value

    def __setattr__(self, name, value):
        raise TypeError("ValueObject objects are immutable")

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def from_value(cls, value):
        return cls(value=value)

    @validator("value")
    def validate_value(cls, value):
        if value is None:
            raise InvalidValueObject()
        return value
