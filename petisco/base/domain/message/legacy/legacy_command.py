from __future__ import annotations

import json
from typing import Any, TypeVar

from petisco.base.domain.message.legacy.legacy_message import LegacyMessage

T = TypeVar("T", bound="LegacyCommand")


class LegacyCommand(LegacyMessage):
    """
    A base class to model your Command.
    An operation that effects some change to the system (for example, modify the persistence).
    An operation that intentionally creates a side effect.
    """

    def __init__(self, **data: Any) -> None:
        self._set_data()
        self._set_attributes(**data)
        self._message_type = "command"  # noqa

    @staticmethod
    def from_dict(
        message_data: dict[str, Any], target_type: type[T] | None = None
    ) -> T:
        target_type = LegacyCommand if target_type is None else target_type
        data = message_data.get("data")
        command = target_type()
        command._set_data(**data)  # type: ignore
        return command

    @staticmethod
    def from_json(message_json: str | bytes, target_type: type[T] | None = None) -> T:
        event_dict = json.loads(message_json)
        return LegacyCommand.from_dict(event_dict, target_type)

    def __repr__(self) -> str:
        return self.to_str(class_name="Command", type="command")
