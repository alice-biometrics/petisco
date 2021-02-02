from typing import Any

from meiga import Error

from petisco.domain.base_object import BaseObject
from dataclasses_json import config
from dataclasses import field, MISSING

ValueObject = BaseObject

ValueObjectError = Error


def value_object_field(value_object_class=ValueObject, default: Any = MISSING):
    def _field():
        return field(
            default=default,
            metadata=config(
                encoder=lambda result: result.value if result else None,
                decoder=lambda value: value_object_class(value) if value else None,
            ),
        )

    return _field()
