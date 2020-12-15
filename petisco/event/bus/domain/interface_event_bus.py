import copy
from typing import Dict
from abc import ABCMeta, abstractmethod

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.event.shared.domain.event import Event, Events


class IEventBus:

    __metaclass__ = ABCMeta

    @classmethod
    def __repr__(cls):
        return f"{cls.__name__}"

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    def _set_info_id(self, info_id: InfoId):
        self.info_id = info_id

    def with_info_id(self, info_id: InfoId):
        event_bus = copy.copy(self)
        event_bus._set_info_id(info_id)
        return event_bus

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
