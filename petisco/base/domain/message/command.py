import json
from typing import Dict, Optional, Type

from petisco.base.domain.message.message import Message


class Command(Message):
    def __init__(self, **kwargs):
        self.type = "command"
        for k in kwargs:
            self.attributes[k] = kwargs[k]

    @staticmethod
    def from_dict(message_data: Dict, target_type: Optional[Type] = None):
        target_type = Command if target_type is None else target_type
        data = message_data.get("data")
        command = target_type()
        command._set_data(**data)
        return command

    @staticmethod
    def from_json(message_json: str, target_type: Optional[Type] = None):
        event_dict = json.loads(message_json)
        return Command.from_dict(event_dict, target_type)

    @classmethod
    def __repr__(cls):
        return cls.to_str(type="command")
