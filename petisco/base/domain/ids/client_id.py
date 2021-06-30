import re

from pydantic import validator

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.model.value_object import ValueObject


class InvalidClientId(DomainEvent):
    def detail(self) -> str:
        return f"Invalid ClientId{self.detail()}"


class ClientId(ValueObject):
    _allow_utf8mb4: bool = True

    @validator("value")
    def validate_value(cls, value):
        if len(value) > 50:
            raise InvalidClientId(uuid_value=value)

        if not isinstance(value, str) or not re.search(
            r"^[\w]*(([',. -][\s]?[\w]?)?[\w]*)*$", value
        ):
            raise InvalidClientId(uuid_value=value)
        if not cls._allow_utf8mb4 and re.match("[^\u0000-\uffff]", value):
            raise InvalidClientId(uuid_value=value)

        return value.title()
