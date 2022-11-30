from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any, Dict, cast

from petisco.base.domain.model.uuid import Uuid
from petisco.base.domain.model.value_object import ValueObject

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_version(config: dict[str, Any] | None) -> int:
    version = getattr(config, "version", 1) if config else 1
    return version


def get_message_name(namespace: dict[str, Any]) -> str:
    return (
        re.sub(r"(?<!^)(?=[A-Z])", "_", namespace.get("__qualname__", "message"))
        .lower()
        .replace("_", ".")
    )


class MetaMessage(type):
    def __new__(
        mcs, name: str, bases: tuple[Any], namespace: dict[str, Any]
    ) -> MetaMessage:
        config = namespace.get("Config")

        namespace["version"] = get_version(config)
        namespace["name"] = get_message_name(namespace)
        namespace["attributes"] = {}
        namespace["meta"] = {}

        return super().__new__(mcs, name, bases, namespace)


class Message(metaclass=MetaMessage):
    message_id: Uuid
    name: str
    version: int
    occurred_on: datetime
    attributes: dict[str, Any]
    meta: dict[str, Any]
    type: str = "message"

    def __init__(self, **data: Any) -> None:
        self.message_id: Uuid
        self.name: str
        self.version: int
        self.occurred_on: datetime
        self.attributes: dict[str, Any] = {}
        self.meta: dict[str, Any] = {}
        self.type: str = "message"
        self._set_data(**data)

    def _set_data(self, **kwargs: dict[str, Any] | None) -> None:
        if kwargs:
            self.message_id = (
                Uuid.from_value(kwargs.get("id")) if kwargs.get("id") else Uuid.v4()
            )
            self.name = str(kwargs.get("type"))
            self.version = cast(int, (kwargs.get("version")))
            self.occurred_on = (
                datetime.strptime(str(kwargs.get("occurred_on")), TIME_FORMAT)
                if kwargs.get("occurred_on")
                else datetime.now()
            )
            self.attributes = cast(Dict[str, Any], kwargs.get("attributes"))
            self.meta = cast(Dict[str, Any], kwargs.get("meta"))
            self.type = str(kwargs.get("type_message", "message"))
        else:
            self.message_id = Uuid.v4()
            self.occurred_on = datetime.utcnow()

    def _set_attributes(self, **data: Any) -> None:
        if self.attributes is None:
            self.attributes = {}
        for k in data:
            self.attributes[k] = data[k]

    def add_meta(self, meta: dict[str, Any]) -> None:
        self.meta = meta

    def update_meta(self, meta: dict[str, Any]) -> Message:
        if not meta:
            return self

        if not isinstance(meta, Dict):
            raise TypeError("Message.update_meta() expect a dict")
        if self.meta:
            self.meta = {**self.meta, **meta}
        else:
            self.meta = meta
        return self

    @staticmethod
    def from_dict(message_data: dict[str, Any]) -> Message:
        data = cast(Dict[str, Any], message_data.get("data"))
        return Message(**data)

    @staticmethod
    def from_json(message_json: str | bytes) -> Message:
        event_dict = json.loads(message_json)
        return Message.from_dict(event_dict)

    def _get_serialized_attributes(self) -> dict[str, Any]:
        attributes = {}
        for key, attribute in self.attributes.items():
            serialized_value = attribute
            if isinstance(attribute, ValueObject):
                serialized_value = attribute.value
            if isinstance(attribute, datetime):
                serialized_value = attribute.strftime(TIME_FORMAT)
            attributes[key] = serialized_value
        return attributes

    def dict(self) -> dict[str, dict[str, Any]]:
        data = {
            "data": {
                "id": self.message_id.value,
                "type": self.name,
                "type_message": self.type,
                "version": self.version,
                "occurred_on": self.occurred_on.strftime(TIME_FORMAT),
                "attributes": self._get_serialized_attributes(),
                "meta": self.meta,
            }
        }
        return data

    def to_str(self, class_name: str = "Message", type: str = "message") -> str:
        return f"{class_name} [{self.message_id.value} ({type}), {self.name} (v{self.version}), {self.occurred_on}, attributes={self.attributes}]"

    def json(self) -> str:
        return json.dumps(self.dict())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Message):
            return False
        return self.dict() == other.dict()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.to_str()
