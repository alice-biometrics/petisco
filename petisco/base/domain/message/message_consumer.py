from abc import abstractmethod
from typing import List, NoReturn, Type

from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.base.misc.interface import Interface


class MessageConsumer(Interface):
    @classmethod
    def __repr__(cls) -> str:
        return cls.__name__

    @abstractmethod
    def add_subscribers(self, subscribers: List[MessageSubscriber]) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_subscriber_on_dead_letter(
        self, subscriber: Type[MessageSubscriber]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_subscriber_on_queue(
        self,
        queue_name: str,
        subscriber: Type[MessageSubscriber],
        is_store: bool = False,
        message_type_expected: str = "message",
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def unsubscribe_subscriber_on_queue(self, queue_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def resume_subscriber_on_queue(self, queue_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def start(self) -> NoReturn:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError
