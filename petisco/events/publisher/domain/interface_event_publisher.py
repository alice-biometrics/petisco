from typing import Dict, List
from abc import ABCMeta, abstractmethod


from petisco.events.event import Event


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

    def publish_list(self, events: List[Event]):
        for event in events:
            self.publish(event)
