from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any, cast

from pydantic import BaseModel

from petisco.base.domain.message.legacy.use_legacy_implementation import (
    USE_LEGACY_IMPLEMENTATION,
)
from petisco.base.domain.model.uuid import Uuid
from petisco.base.domain.model.value_object import ValueObject

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_version(config: dict[str, Any] | None) -> int:
    version = getattr(config, "version", 1) if config else 1
    return version


class Message(BaseModel):
    def model_post_init(self, __context: Any) -> None:
        if not hasattr(self, "_message_attributes"):
            attributes = dict(self)
            if "_message_type" in attributes:
                attributes.pop("_message_type")
            self._message_attributes = attributes

        if not hasattr(self, "_message_formatted_message"):
            self._message_formatted_message = None  # noqa

        if self._message_formatted_message:
            # print("_message_formatted_message exist")
            self._update_from_formatted_message()
        # else:
        # print("_message_formatted_message dont exist")

        if not hasattr(self, "_message_id"):
            self._message_id = Uuid.v4()  # noqa

        if not hasattr(self, "_message_name"):
            self._message_name = (  # noqa
                re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__)
                .lower()
                .replace("_", ".")
            )
        if hasattr(self, "Config"):
            self._message_version = get_version(self.Config)
        else:
            self._message_version = 1  # noqa

        if not hasattr(self, "_message_occurred_on"):
            self._message_occurred_on = datetime.utcnow()  # noqa

        if not hasattr(self, "_message_attributes"):
            self._message_attributes = dict()  # noqa

        if not hasattr(self, "_message_meta"):
            self._message_meta = dict()  # noqa

        if not hasattr(self, "_message_type"):
            self._message_type = "message"  # noqa

        # To serialize ValueObjects (seems not working)
        # for key, attribute in self._message_attributes.items():
        #     if issubclass(attribute.__class__, ValueObject):
        #         print(key)
        #         setattr(self, f"_{key}", ValueObject.serializer(key))

    def add_meta(self, meta: dict[str, Any]) -> None:
        self._message_meta = meta

    def update_meta(self, meta: dict[str, Any]) -> Message:
        if not meta:
            return self

        if not isinstance(meta, dict):
            raise TypeError("Message.update_meta() expect a dict")
        if self._message_meta:
            self._message_meta = {**self._message_meta, **meta}
        else:
            self._message_meta = meta
        return self

    def format(self) -> dict[str, dict[str, Any]]:
        data = {
            "data": {
                "id": self._message_id.value,
                "type": self._message_name,
                "type_message": self._message_type,
                "version": self._message_version,
                "occurred_on": self._message_occurred_on.strftime(TIME_FORMAT),
                "attributes": self._get_serialized_attributes(),
                "meta": self._message_meta,
            }
        }
        return data

    def format_json(self) -> str:
        return json.dumps(self.format())

    @classmethod
    def from_format(
        cls,
        formatted_message: dict[str, Any] | str | bytes,
        target_type: type | None = None,
    ) -> Message:
        if not isinstance(formatted_message, dict):
            formatted_message = json.loads(formatted_message)
        data = cast(dict[str, Any], formatted_message.get("data"))
        attributes = data.get("attributes", dict())
        # attributes.update({"formatted_message": data})

        # data = message_data.get("data")
        # domain_event = target_type()
        target_type = target_type if target_type else cls
        message = target_type(**attributes)
        message._message_formatted_message = data
        message._update_from_formatted_message()
        return message

    def _get_serialized_attributes(self) -> dict[str, Any]:
        attributes = {}
        for key, attribute in self._message_attributes.items():
            serialized_value = attribute
            if isinstance(attribute, ValueObject):
                serialized_value = attribute.value
            if isinstance(attribute, datetime):
                serialized_value = attribute.strftime(TIME_FORMAT)
            attributes[key] = serialized_value
        return attributes

    def _update_from_formatted_message(self) -> None:
        kwargs = self._message_formatted_message
        # print("Message _update_from_formatted_message")
        self._message_id = (
            Uuid.from_value(kwargs.get("id")) if kwargs.get("id") else Uuid.v4()
        )
        self._message_name = str(kwargs.get("type"))
        self._message_version = int(kwargs.get("version", 1))
        self._message_occurred_on = (
            datetime.strptime(str(kwargs.get("occurred_on")), TIME_FORMAT)
            if kwargs.get("occurred_on")
            else datetime.now()
        )

        attributes = kwargs.get("attributes", dict())
        self._message_attributes = cast(dict[str, Any], attributes)
        # for k in attributes:
        #     self._message_attributes[k] = attributes[k]
        #     setattr(self, k, attributes[k])

        self._message_meta = cast(dict[str, Any], kwargs.get("meta"))
        self._message_type = str(kwargs.get("type_message", "message"))
        # for key, value in self._message_attributes.items():
        #     setattr(self, key, value)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Message):
            return False
        return self.format() == other.format()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self._message_type} [{self._message_id.value} ({self._message_type}), {self._message_name} (v{self._message_version}), {self._message_occurred_on}, attributes={self._message_attributes}]"

    def get_message_id(self) -> Uuid:
        return self._message_id

    def get_message_name(self) -> str:
        return self._message_name

    def get_message_version(self) -> int:
        return self._message_version

    def get_message_occurred_on(self) -> datetime:
        return self._message_occurred_on

    def get_message_attributes(self) -> dict[str, Any]:
        return self._message_attributes

    def get_message_meta(self) -> dict[str, Any]:
        return self._message_meta

    def get_message_type(self) -> str:
        return self._message_type


if USE_LEGACY_IMPLEMENTATION is True:
    from petisco.base.domain.message.legacy.legacy_message import LegacyMessage  # noqa

    Message = LegacyMessage  # noqa
