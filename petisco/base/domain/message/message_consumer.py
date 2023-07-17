from __future__ import annotations

from abc import abstractmethod
from typing import Generic, NoReturn, TypeVar

from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.base.misc.interface import Interface

T = TypeVar("T", bound=MessageSubscriber)


class MessageConsumer(Generic[T], Interface):
    """
    A base class to implement an infrastructure-based consumer to link received messages from rabbitmq with
    defined subscribers.
    """

    @classmethod
    def __repr__(cls) -> str:
        return cls.__name__

    @abstractmethod
    def add_subscribers(self, subscribers: list[type[T]]) -> None:
        """
        Add defined subscribers to be connected with main queues.
        """
        raise NotImplementedError

    @abstractmethod
    def add_subscriber_on_dead_letter(self, subscriber: type[T]) -> None:
        """
        Add defined subscribers to be connected with the correspondent dead letter.
        """
        raise NotImplementedError

    @abstractmethod
    def add_subscriber_on_queue(
        self,
        queue_name: str,
        subscriber: type[T],
        is_store: bool = False,
        message_type_expected: str = "message",
    ) -> None:
        """
        Add defined subscribers to be connected with a specific queue name.
        """
        raise NotImplementedError

    @abstractmethod
    def unsubscribe_subscriber_on_queue(self, queue_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def resume_subscriber_on_queue(self, queue_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def start(self) -> NoReturn:
        """
        Start the process of consuming messages from infrastructure and pass to subscriber.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the process of consuming messages from infrastructure.
        """
        raise NotImplementedError
