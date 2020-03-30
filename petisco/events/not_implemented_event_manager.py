from typing import Dict, Callable

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.events.event import Event
from petisco.events.interface_event_manager import IEventManager


class NotImplementedEventManager(IEventManager):
    def __init__(self, subscribers: Dict[str, Callable] = None):
        super().__init__(subscribers)

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def unsubscribe_all(self):
        pass

    def publish(self, topic: str, event: Event, info_id: InfoId = None):
        pass
