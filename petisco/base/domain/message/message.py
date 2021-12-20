import json
import re
from datetime import datetime
from typing import Dict

from petisco.base.domain.model.uuid import Uuid
from petisco.base.domain.model.value_object import ValueObject

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_version(config) -> int:
    version = getattr(config, "version", 1) if config else 1
    return version


def get_message_name(namespace) -> str:
    return (
        re.sub(r"(?<!^)(?=[A-Z])", "_", namespace.get("__qualname__", "message"))
        .lower()
        .replace("_", ".")
    )


class MetaMessage(type):
    def __new__(mcs, name, bases, namespace):
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
    attributes: Dict
    meta: Dict
    type: str = "message"

    def __init__(self, **kwargs):
        self._set_data(**kwargs)

    def _set_data(self, **kwargs):
        if kwargs:
            self.message_id = (
                Uuid.from_value(kwargs.get("id")) if kwargs.get("id") else Uuid.v4()
            )
            self.name = kwargs.get("type")
            self.version = kwargs.get("version")
            self.occurred_on = (
                datetime.strptime(kwargs.get("occurred_on"), TIME_FORMAT)
                if kwargs.get("occurred_on")
                else datetime.now()
            )
            self.attributes = kwargs.get("attributes")
            self.meta = kwargs.get("meta")
            self.type = kwargs.get("type_message", "message")
        else:
            self.message_id = Uuid.v4()
            self.occurred_on = datetime.utcnow()

    def _set_attributes(self, **kwargs):
        if self.attributes is None:
            self.attributes = {}
        for k in kwargs:
            self.attributes[k] = kwargs[k]

    def add_meta(self, meta: Dict):
        self.meta = meta

    def update_meta(self, meta: Dict):
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
    def from_dict(message_data: Dict):
        data = message_data.get("data")
        return Message(**data)

    @staticmethod
    def from_json(message_json: str):
        event_dict = json.loads(message_json)
        return Message.from_dict(event_dict)

    def _get_serialized_attributes(self) -> Dict:
        attributes = {}
        for key, attribute in self.attributes.items():
            serialized_value = attribute
            if isinstance(attribute, ValueObject):
                serialized_value = attribute.value
            if isinstance(attribute, datetime):
                serialized_value = attribute.strftime(TIME_FORMAT)
            attributes[key] = serialized_value
        return attributes

    def dict(self) -> Dict:
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

    def to_str(self, class_name="Message", type: str = "message"):
        return f"{class_name} [{self.message_id.value} ({type}), {self.name} (v{self.version}), {self.occurred_on}, attributes={self.attributes}]"

    def json(self):
        return json.dumps(self.dict())

    def __eq__(self, other):
        return self.dict() == other.dict()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.to_str()
