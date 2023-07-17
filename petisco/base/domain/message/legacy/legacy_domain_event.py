from __future__ import annotations

import json
from typing import Any, TypeVar

from petisco.base.domain.message.legacy.legacy_message import LegacyMessage

T = TypeVar("T", bound="LegacyDomainEvent")


class LegacyDomainEvent(LegacyMessage):
    """
    A base class to model your domain events.
    Define your Domain Events to express what happened in your domain.
    """

    def __init__(self, **data: Any) -> None:
        super().__init__()
        self._set_attributes(**data)
        self._message_type = "domain_event"

    @staticmethod
    def from_dict(
        message_data: dict[str, Any],
        target_type: type[T] | None = None,
    ) -> T:
        target_type = LegacyDomainEvent if target_type is None else target_type
        data = message_data.get("data")
        domain_event = target_type()
        domain_event._set_data(**data)  # type: ignore
        return domain_event

    @staticmethod
    def from_json(
        message_json: str | bytes,
        target_type: type[T] | None = None,
    ) -> T:
        event_dict = json.loads(message_json)
        return LegacyDomainEvent.from_dict(event_dict, target_type)

    def __repr__(self) -> str:
        return self.to_str(class_name="DomainEvent", type="domain_event")
