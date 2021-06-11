import json
import re
from datetime import datetime
from typing import Dict

from petisco.base.domain.model.uuid import Uuid

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

        namespace["message_id"] = Uuid.v4()
        namespace["version"] = get_version(config)
        namespace["occurred_on"] = datetime.now()
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
        if kwargs:
            self.message_id = Uuid.from_value(kwargs.get("id"))
            self.name = kwargs.get("type")
            self.version = kwargs.get("version")
            self.occurred_on = datetime.strptime(kwargs.get("occurred_on"), TIME_FORMAT)
            self.attributes = kwargs.get("attributes")
            self.meta = kwargs.get("meta")
            self.type = kwargs.get("type_message", "message")

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

    def dict(self) -> Dict:
        data = {
            "data": {
                "id": self.message_id.value,
                "type": self.name,
                "type_message": self.type,
                "version": self.version,
                "occurred_on": self.occurred_on.strftime(TIME_FORMAT),
                "attributes": self.attributes,
                "meta": self.meta,
            }
        }
        return data

    def json(self):
        return json.dumps(self.dict())

    def __eq__(self, other):
        return self.dict() == other.dict()

    @classmethod
    def __str__(cls):
        return cls.__repr__()

    @classmethod
    def __repr__(cls):
        return f"{cls.__name__} [{cls.message_id.value} ({cls.type}), {cls.name} (v{cls.version}), {cls.occurred_on}, attributes={cls.attributes}]"
