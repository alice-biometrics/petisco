from typing import Dict
from abc import ABCMeta, abstractmethod


from petisco.event.shared.domain.event import Event, Events


class IEventBus:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return f"IEventBus"

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
    def retry_publish_only_on_store_queue(self, event: Event):
        raise NotImplementedError

    def retry_publish_events_only_on_store_queue(self, events: Events):
        for event in events:
            self.retry_publish_only_on_store_queue(event)

    @abstractmethod
    def stop(self):
        raise NotImplementedError
