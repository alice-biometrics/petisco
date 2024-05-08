import os
from typing import Any, Union
from uuid import UUID, uuid4

import validators
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from petisco.base.domain.errors.defaults.invalid_uuid import InvalidUuid

USE_LEGACY_UUID = bool(os.getenv("USE_LEGACY_UUID", "False").lower() == "true")


class Uuid(str):
    def __new__(cls, value: Union[str, UUID]) -> "Uuid":
        if value is None or not validators.uuid(str(value)):
            raise InvalidUuid(uuid_value=str(value))
        return super().__new__(cls, str(value))

    @classmethod
    def v4(cls) -> "Uuid":
        return cls(str(uuid4()))

    @property
    def value(self) -> str:
        return self

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * str will be parsed as `Uuid` instances with the str as the value attribute
        * `Uuid` instances will be parsed as `Uuid` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just a str
        """

        def validate_from_str(value: str) -> "Uuid":
            return Uuid(value)

        from_uuid_schema = core_schema.chain_schema(
            [
                core_schema.uuid_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_uuid_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(Uuid),
                    from_uuid_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(lambda instance: instance.value),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `uuid`
        return handler(core_schema.uuid_schema())


if USE_LEGACY_UUID is True:
    from petisco.base.domain.model.legacy_uuid import LegacyUuid  # noqa

    Uuid = LegacyUuid  # noqa
