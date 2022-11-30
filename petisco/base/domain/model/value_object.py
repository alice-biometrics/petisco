from typing import Any, NoReturn, Type, TypeVar

from pydantic import validator
from pydantic.main import BaseModel

from petisco.base.domain.errors.defaults.invalid_value_object import InvalidValueObject

TypeValueObject = TypeVar("TypeValueObject", bound="ValueObject")


class ValueObject(BaseModel):
    """
    A base class to define ValueObject

    It is small object that represents a simple entity whose equality is not based on identity.
    """

    value: Any

    def __init__(self, value: Any, **data: Any) -> None:
        super().__init__(value=value, **data)

    def dict(self, **kwargs: Any) -> Any:
        return self.value

    def __setattr__(self, name: str, value: Any) -> NoReturn:
        raise TypeError("ValueObject objects are immutable")

    def __hash__(self) -> int:
        return hash(self.value)

    @classmethod
    def from_value(cls: Type[TypeValueObject], value: Any) -> TypeValueObject:
        return cls(value=value)

    @validator("value")
    def validate_value(cls, value: Any) -> Any:
        if value is None:
            raise InvalidValueObject()
        return value
