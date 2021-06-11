from typing import Dict, List, Callable
from abc import abstractmethod, ABC

from petisco.base.domain.message.message_subscriber import MessageSubscriber


class MessageConsumer(ABC):
    @classmethod
    def __repr__(cls):
        return cls.__name__

    @classmethod
    def info(cls) -> Dict:
        return {"name": cls.__name__}

    @abstractmethod
    def add_subscribers(self, subscribers: List[MessageSubscriber]):
        raise NotImplementedError

    @abstractmethod
    def add_subscriber_on_dead_letter(
        self, subscriber: MessageSubscriber, handler: Callable
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
