from typing import Dict, Callable

from petisco.events.event import Event
from petisco.events.interface_event_manager import IEventManager


class FakeEventManager(IEventManager):

    is_subscribed = False

    def __init__(self, subscribers: Dict[str, Callable]):
        super().__init__(subscribers)
        if subscribers:
            self.is_subscribed = True

    def unsubscribe_all(self):
        self.is_subscribed = False

    def send(self, topic: str, event: Event):
        if self.is_subscribed and topic in self.subscribers:
            self.subscribers.get(topic)(event)
