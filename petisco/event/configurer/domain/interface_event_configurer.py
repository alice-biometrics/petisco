from typing import Dict, List
from abc import ABCMeta, abstractmethod

from petisco.event.shared.domain.event import Event
from petisco.event.shared.domain.event_subscriber import EventSubscriber


class IEventConfigurer:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return f"IEventConfigurer"

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    @abstractmethod
    def configure_subscribers(
        self,
        subscribers: List[EventSubscriber],
        clear_subscriber_before: bool = False,
        clear_store_before: bool = False,
    ):
        raise NotImplementedError

    @abstractmethod
    def configure_event(self, event: Event):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError
