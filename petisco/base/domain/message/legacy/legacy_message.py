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
    message_name = namespace.get("__qualname__", "message")

    if ".<locals>." in message_name:
        message_name = message_name.split(".<locals>.")[-1]
    message_name = message_name.replace("Legacy", "")
    return re.sub(r"(?<!^)(?=[A-Z])", "_", message_name).lower().replace("_", ".")


class MetaMessage(type):
    def __new__(
        mcs, name: str, bases: tuple[Any], namespace: dict[str, Any]
    ) -> MetaMessage:
        config = namespace.get("Config")

        namespace["_message_version"] = get_version(config)
        namespace["_message_name"] = get_message_name(namespace)
        namespace["_message_attributes"] = {}
        namespace["_message_meta"] = {}

        return super().__new__(mcs, name, bases, namespace)


class LegacyMessage(metaclass=MetaMessage):
    _message_id: Uuid
    _message_name: str
    _message_version: int
    _message_occurred_on: datetime
    _message_attributes: dict[str, Any]
    _message_meta: dict[str, Any]
    _message_type: str

    def __init__(self, **data: Any) -> None:
        self._message_attributes = {}
        self._message_meta = {}
        if not hasattr(self, "_message_type"):
            self._message_type = "message"
        self._set_data(**data)

    def _set_data(self, **kwargs: dict[str, Any] | None) -> None:
        if kwargs:
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
            self._message_attributes = cast(Dict[str, Any], kwargs.get("attributes"))
            self._message_meta = cast(Dict[str, Any], kwargs.get("meta"))
            self._message_type = str(kwargs.get("type_message", self._message_type))

            if self._message_attributes:
                for key, value in self._message_attributes.items():
                    setattr(self, key, value)
        else:
            self._message_id = Uuid.v4()
            self._message_occurred_on = datetime.utcnow()

    def _set_attributes(self, **data: Any) -> None:
        if self._message_attributes is None:
            self._message_attributes = {}
        for k in data:
            self._message_attributes[k] = data[k]
            setattr(self, k, data[k])

    def add_meta(self, meta: dict[str, Any]) -> None:
        self._message_meta = meta

    def update_meta(self, meta: dict[str, Any]) -> LegacyMessage:
        if not meta:
            return self

        if not isinstance(meta, Dict):
            raise TypeError("Message.update_meta() expect a dict")
        if hasattr(self, "_message_meta"):
            self._message_meta = {**self._message_meta, **meta}
        else:
            self._message_meta = meta
        return self

    @staticmethod
    def from_dict(message_data: dict[str, Any]) -> LegacyMessage:
        data = cast(Dict[str, Any], message_data.get("data"))
        return LegacyMessage(**data)

    @staticmethod
    def from_json(message_json: str | bytes) -> LegacyMessage:
        event_dict = json.loads(message_json)
        return LegacyMessage.from_dict(event_dict)

    @classmethod
    def from_format(
        cls,
        formatted_message: dict[str, Any] | str | bytes,
        target_type: type | None = None,
    ) -> LegacyMessage:
        if not isinstance(formatted_message, dict):
            formatted_message = json.loads(formatted_message)
        return cls.from_dict(formatted_message)

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

    def dict(self) -> dict[str, dict[str, Any]]:
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

    def model_dump(self) -> dict[str, dict[str, Any]]:
        return self.dict()

    def format(self) -> dict[str, dict[str, Any]]:
        # To improve migration
        return self.dict()

    def format_json(self) -> str:
        # To improve migration
        return json.dumps(self.format())

    def to_str(self, class_name: str = "Message", type: str = "message") -> str:
        return f"{class_name} [{self._message_id.value} ({type}), {self._message_name} (v{self._message_version}), {self._message_occurred_on}, attributes={self._message_attributes}]"

    def json(self) -> str:
        return json.dumps(self.dict())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LegacyMessage):
            return False
        return self.dict() == other.dict()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.to_str()

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
