from typing import Any

from pydantic.main import BaseModel


class ValueObject(BaseModel):
    value: Any

    def dict(self, **kwargs):
        return self.value

    def __setattr__(self, name, value):
        raise TypeError("ValueObject objects are immutable")

    @classmethod
    def from_value(cls, value):
        return cls(value=value)
