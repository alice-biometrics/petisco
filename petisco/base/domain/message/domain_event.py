import json
from typing import Any, Dict, Optional, Type, Union

from petisco.base.domain.message.message import Message


class DomainEvent(Message):
    """
    A base class to model your domain events.
    Define your Domain Events to express what happened in your domain.
    """

    def __init__(self, **data: Any) -> None:
        super().__init__()
        self._set_attributes(**data)
        self.type = "domain_event"

    @staticmethod
    def from_dict(
        message_data: Dict[str, Any],
        target_type: Union[Type["DomainEvent"], None] = None,
    ) -> "DomainEvent":
        target_type = DomainEvent if target_type is None else target_type
        data = message_data.get("data")
        domain_event = target_type()
        domain_event._set_data(**data)  # type: ignore
        return domain_event

    @staticmethod
    def from_json(
        message_json: Union[str, bytes],
        target_type: Optional[Type["DomainEvent"]] = None,
    ) -> "DomainEvent":
        event_dict = json.loads(message_json)
        return DomainEvent.from_dict(event_dict, target_type)

    def __repr__(self) -> str:
        return self.to_str(class_name="DomainEvent", type="domain_event")
