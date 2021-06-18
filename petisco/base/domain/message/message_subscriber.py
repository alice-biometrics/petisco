from typing import List, Callable

from dataclasses import dataclass

from petisco.base.domain.message.message import Message


@dataclass
class MessageSubscriber:
    message_name: str
    message_version: int
    message_type: str
    handlers: List[Callable]

    def get_handlers_names(self) -> List[str]:
        return [handler.__name__ for handler in self.handlers]

    @classmethod
    def get_full_handlers_path(cls) -> List[str]:
        return [f"{handler.__module__}.{handler.__name__}" for handler in cls.handlers]

    @classmethod
    def __repr__(cls):
        return f"{cls.__name__} ({cls.message_name}.{cls.message_version} ({cls.message_type}) -> {cls.get_full_handlers_path()})"

    @staticmethod
    def from_message(message: Message, handlers: List[Callable]):
        return MessageSubscriber(
            message_name=message.name,
            message_version=message.version,
            message_type=message.type,
            handlers=handlers,
        )
