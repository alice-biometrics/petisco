from typing import List

from petisco.event.shared.domain.event import Event
from petisco.event.shared.domain.event_subscriber import EventSubscriber
from petisco.event.configurer.domain.interface_event_configurer import IEventConfigurer


class NotImplementedEventConfigurer(IEventConfigurer):
    def configure(self):
        self.configure_subscribers([])

    def configure_event(self, event: Event):
        self.configure_subscribers(
            [
                EventSubscriber(
                    event_name=event.event_name,
                    event_version=event.event_version,
                    handlers=[],
                )
            ]
        )

    def configure_subscribers(self, subscribers: List[EventSubscriber]):
        pass

    def clear(self):
        pass
