from typing import Any, NoReturn, Type, TypeVar

from pydantic import BaseModel, PlainSerializer, field_serializer, field_validator

from petisco.base.domain.errors.defaults.invalid_value_object import InvalidValueObject

TypeValueObject = TypeVar("TypeValueObject", bound="ValueObject")


ValueObjectSerializer = PlainSerializer(lambda value_object: value_object.value if value_object else None)


class ValueObject(BaseModel):
    """
    A base class to define ValueObject

    It is small object that represents a simple entity whose equality is not based on identity.
    """

    value: Any = None

    def __init__(self, value: Any, **data: Any) -> None:
        super().__init__(value=value, **data)

    def model_dump(self, **kwargs: Any) -> Any:
        return self.value

    def dict(self, **kwargs: Any) -> Any:
        return self.model_dump(**kwargs)

    # The following is working serializing but it is a problem deserializing
    # @model_serializer
    # def serialize_model(self) -> Any:
    #     return self.value
    #
    # if TYPE_CHECKING:
    #     # Ensure type checkers see the correct return type
    #     # from https://docs.pydantic.dev/latest/usage/serialization/#overriding-the-return-type-when-dumping-a-model
    #     def model_dump(
    #         self,
    #         *,
    #         mode: Literal['json', 'python'] | str = 'python',
    #         include: Any = None,
    #         exclude: Any = None,
    #         by_alias: bool = False,
    #         exclude_unset: bool = False,
    #         exclude_defaults: bool = False,
    #         exclude_none: bool = False,
    #         round_trip: bool = False,
    #         warnings: bool = True,
    #     ) -> Any:
    #         ...

    def __setattr__(self, name: str, value: Any) -> NoReturn:
        raise TypeError("ValueObject objects are immutable")

    def __hash__(self) -> int:
        return hash(self.value)

    @classmethod
    def from_value(cls: Type[TypeValueObject], value: Any) -> TypeValueObject:
        return cls(value=value)

    @field_validator("value")
    def validate_value(cls, value: Any) -> Any:
        if value is None:
            raise InvalidValueObject()
        return value

    @staticmethod
    def serializer(attribute_name: str) -> Any:
        def _serializer(value_object: ValueObject) -> Any:
            if value_object:
                return value_object.value

        return field_serializer(attribute_name)(_serializer)
