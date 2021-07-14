from abc import abstractmethod
from typing import Callable, List, Type

from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.base.misc.interface import Interface


class MessageConsumer(Interface):
    @classmethod
    def __repr__(cls):
        return cls.__name__

    @abstractmethod
    def add_subscribers(self, subscribers: List[MessageSubscriber]):
        raise NotImplementedError

    @abstractmethod
    def add_subscriber_on_dead_letter(self, subscriber: Type[MessageSubscriber]):
        raise NotImplementedError

    @abstractmethod
    def add_subscriber_on_queue(self, queue_name: str, handler: Callable):
        raise NotImplementedError

    @abstractmethod
    def unsubscribe_subscriber_on_queue(self, queue_name: str):
        raise NotImplementedError

    @abstractmethod
    def resume_subscriber_on_queue(self, queue_name: str):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
