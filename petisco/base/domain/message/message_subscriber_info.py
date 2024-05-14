from __future__ import annotations

import re

from pydantic.main import BaseModel

from petisco.base.domain.message.command import Command
from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message import Message


class MessageSubscriberInfo(BaseModel):
    message_name: str
    message_version: int
    message_type: str

    @staticmethod
    def from_class_type(class_type: type[Message]) -> MessageSubscriberInfo:
        message_name = (  # noqa
            re.sub(r"(?<!^)(?=[A-Z])", "_", class_type.__name__).lower().replace("_", ".")
        )

        message_version = 1
        if hasattr(class_type, "Config") and hasattr(class_type.Config, "version"):
            message_version = int(class_type.Config.version)

        message_type = "message"
        if issubclass(class_type, DomainEvent):
            message_type = "domain_event"
        elif issubclass(class_type, Command):
            message_type = "command"

        return MessageSubscriberInfo(
            message_name=message_name,
            message_version=message_version,
            message_type=message_type,
        )
