from typing import Dict

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.events.event import Event
from petisco.events.interface_event_manager import IEventManager


class FakeEventManager(IEventManager):
    def __init__(self):
        self.sent_events = {}

    def info(self) -> Dict:
        pass

    def unsubscribe_all(self):
        pass

    def publish(self, topic: str, event: Event, info_id: InfoId = None):

        if topic not in self.sent_events:
            self.sent_events[topic] = [event]
        else:
            self.sent_events[topic].append(event)

    def get_sent_events(self, topic):
        return self.sent_events[topic]
