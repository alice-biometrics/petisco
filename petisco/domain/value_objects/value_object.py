from meiga import Error

from petisco.domain.base_object import BaseObject
from dataclasses_json import config
from dataclasses import field

ValueObject = BaseObject

ValueObjectError = Error


def value_object_field(value_object_class=ValueObject):
    def _field():
        return field(
            metadata=config(
                encoder=lambda result: result.value,
                decoder=lambda value: value_object_class(value),
            )
        )

    return _field()
