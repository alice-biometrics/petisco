from typing import Type

from pydantic.main import BaseModel

from petisco.base.domain.message.message import Message


class MessageSubscriberInfo(BaseModel):
    message_name: str
    message_version: int
    message_type: str

    @staticmethod
    def from_class_type(class_type: Type[Message]):
        message = class_type()
        return MessageSubscriberInfo(
            message_name=message.name,
            message_version=message.version,
            message_type=message.type,
        )
