from typing import List, Callable

from dataclasses import dataclass

from petisco import Event


@dataclass
class EventSubscriber:
    event: Event
    handlers: List[Callable]

    def get_handlers_names(self) -> List[str]:
        return [handler.__name__ for handler in self.handlers]
