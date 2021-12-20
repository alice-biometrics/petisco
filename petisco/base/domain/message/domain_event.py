import json
from typing import Dict, Optional, Type, Union

from petisco.base.domain.message.message import Message


class DomainEvent(Message):
    def __init__(self, **kwargs):
        self._set_data()
        self._set_attributes(**kwargs)
        self.type = "domain_event"

    @staticmethod
    def from_dict(message_data: Dict, target_type: Optional[Type] = None):
        target_type = DomainEvent if target_type is None else target_type
        data = message_data.get("data")
        domain_event = target_type()
        domain_event._set_data(**data)
        return domain_event

    @staticmethod
    def from_json(message_json: Union[str, bytes], target_type: Optional[Type] = None):
        event_dict = json.loads(message_json)
        return DomainEvent.from_dict(event_dict, target_type)

    def __repr__(self):
        return self.to_str(class_name="DomainEvent", type="domain_event")
