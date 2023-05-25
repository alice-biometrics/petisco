from __future__ import annotations

from pydantic.main import BaseModel

from petisco.base.domain.message.message import Message


class MessageSubscriberInfo(BaseModel):
    message_name: str
    message_version: int
    message_type: str

    @staticmethod
    def from_class_type(class_type: type[Message]) -> MessageSubscriberInfo:
        message = class_type()
        return MessageSubscriberInfo(
            message_name=message.get_message_name(),
            message_version=message.get_message_version(),
            message_type=message.get_message_type(),
        )
