from typing import Dict
from abc import ABCMeta, abstractmethod


from petisco.event.shared.domain.event import Event, Events


class IEventPublisher:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return f"IEventPublisher"

    @abstractmethod
    def info(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def publish(self, event: Event):
        raise NotImplementedError

    def publish_events(self, events: Events):
        for event in events:
            self.publish(event)

    @abstractmethod
    def stop(self):
        raise NotImplementedError
