from typing import Dict, Callable, List
from abc import ABCMeta, abstractmethod

import deprecation

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.events.event import Event
from petisco import __version__


class IEventManager:

    __metaclass__ = ABCMeta

    def __init__(self, subscribers: Dict[str, Callable]):
        self.subscribers = subscribers

    def __repr__(self):
        return f"EventManager: [subscribers: {self.subscribers}]"

    @abstractmethod
    def info(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe_all(self):
        raise NotImplementedError

    @abstractmethod
    def publish(self, topic: str, event: Event, info_id: InfoId = None):
        raise NotImplementedError

    def publish_list(self, topic: str, events: List[Event], info_id: InfoId = None):
        for event in events:
            self.publish(topic, event, info_id)

    @deprecation.deprecated(
        deprecated_in="0.14.4",
        removed_in="1.0.0",
        current_version=__version__,
        details="Use the publish function instead",
    )
    def send(self, topic: str, event: Event):
        self.publish(topic, event)
