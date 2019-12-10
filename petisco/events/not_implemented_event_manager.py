from typing import Dict, Callable

from petisco.events.event import Event
from petisco.events.interface_event_manager import IEventManager


class NotImplementedEventManager(IEventManager):
    def __init__(self, subscribers: Dict[str, Callable] = None):
        super().__init__(subscribers)

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def unsubscribe_all(self):
        pass

    def send(self, topic: str, event: Event):
        pass
