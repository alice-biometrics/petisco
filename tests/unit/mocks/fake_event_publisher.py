from typing import Dict

from petisco.events.event import Event
from petisco.events.publisher.domain.interface_event_publisher import IEventPublisher


class FakeEventPublisher(IEventPublisher):
    def __init__(self):
        self.sent_events = []

    def info(self) -> Dict:
        pass

    def publish(self, event: Event):
        self.sent_events.append(event)

    def get_sent_events(self):
        return self.sent_events
