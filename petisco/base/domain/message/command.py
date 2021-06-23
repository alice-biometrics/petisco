import json
from typing import Dict

from petisco.base.domain.message.message import Message


class Command(Message):
    def __init__(self, **kwargs):
        self.type = "command"
        for k in kwargs:
            self.attributes[k] = kwargs[k]

    @staticmethod
    def from_dict(message_data: Dict):
        data = message_data.get("data")
        return Command(**data)

    @staticmethod
    def from_json(message_json: str):
        event_dict = json.loads(message_json)
        return Command.from_dict(event_dict)

    @classmethod
    def __repr__(cls):
        return cls.to_str(type="command")
