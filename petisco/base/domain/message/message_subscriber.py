from typing import List, Callable

from dataclasses import dataclass


@dataclass
class MessageSubscriber:
    message_name: str
    message_version: int
    handlers: List[Callable]

    def get_handlers_names(self) -> List[str]:
        return [handler.__name__ for handler in self.handlers]

    @classmethod
    def get_full_handlers_path(cls) -> List[str]:
        return [f"{handler.__module__}.{handler.__name__}" for handler in cls.handlers]

    @classmethod
    def __repr__(cls):
        return f"{cls.__name__} ({cls.message_name}.{cls.message_version} -> {cls.get_full_handlers_path()})"
