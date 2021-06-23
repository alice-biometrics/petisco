import json
from typing import Dict

from petisco.base.domain.message.message import Message


class DomainEvent(Message):
    def __init__(self, **kwargs):
        self.type = "domain_event"
        for k in kwargs:
            self.attributes[k] = kwargs[k]

    @staticmethod
    def from_dict(message_data: Dict):
        data = message_data.get("data")
        return DomainEvent(**data)

    @staticmethod
    def from_json(message_json: str):
        event_dict = json.loads(message_json)
        return DomainEvent.from_dict(event_dict)

    @classmethod
    def __repr__(cls):
        return cls.to_str(type="domain_event")
