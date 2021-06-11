from typing import Dict, List, Callable
from abc import ABCMeta, abstractmethod

from petisco.legacy.event.shared.domain.event_subscriber import EventSubscriber


class IEventConsumer:

    __metaclass__ = ABCMeta

    def __repr__(self):
        return "IEventConsumer"

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    @abstractmethod
    def add_subscribers(self, subscribers: List[EventSubscriber]):
        raise NotImplementedError

    @abstractmethod
    def add_subscriber_on_dead_letter(
        self, subscriber: EventSubscriber, handler: Callable
    ):
        raise NotImplementedError

    @abstractmethod
    def add_handler_on_store(self, handler: Callable):
        raise NotImplementedError

    @abstractmethod
    def add_handler_on_queue(self, queue_name: str, handler: Callable):
        raise NotImplementedError

    @abstractmethod
    def unsubscribe_handler_on_queue(self, queue_name: str):
        raise NotImplementedError

    @abstractmethod
    def resume_handler_on_queue(self, queue_name: str):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
