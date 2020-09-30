from typing import Dict, List, Callable
from abc import ABCMeta, abstractmethod

from petisco.event.shared.domain.event_subscriber import EventSubscriber


class IEventConsumer:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return f"IEventConsumer"

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    @abstractmethod
    def consume_subscribers(self, subscribers: List[EventSubscriber]):
        raise NotImplementedError

    @abstractmethod
    def consume_dead_letter(self, subscriber: EventSubscriber, handler: Callable):
        raise NotImplementedError

    @abstractmethod
    def consume_store(self, handler: Callable):
        raise NotImplementedError

    @abstractmethod
    def consume_queue(self, queue_name: str, handler: Callable):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
