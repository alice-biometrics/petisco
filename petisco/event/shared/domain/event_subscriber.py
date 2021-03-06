from typing import List, Callable

from dataclasses import dataclass


@dataclass
class EventSubscriber:
    event_name: str
    event_version: int
    handlers: List[Callable]

    def get_handlers_names(self) -> List[str]:
        return [handler.__name__ for handler in self.handlers]

    def __repr__(self):
        return f"EventSubscriber ({self.event_name}.{self.event_version} -> {self.handlers})"
