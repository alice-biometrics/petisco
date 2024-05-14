from __future__ import annotations

from typing import Any, NoReturn

from petisco.base.domain.message.message_consumer import MessageConsumer
from petisco.base.domain.message.message_subscriber import MessageSubscriber


class NotImplementedMessageConsumer(MessageConsumer[Any]):
    def start(self) -> NoReturn:
        pass

    def add_subscribers(self, subscribers: list[MessageSubscriber]) -> None:
        pass

    def add_subscriber_on_dead_letter(self, subscriber: type[MessageSubscriber]) -> None:
        pass

    def add_subscriber_on_queue(
        self,
        queue_name: str,
        subscriber: type[MessageSubscriber],
        is_store: bool = False,
        message_type_expected: str = "message",
    ) -> None:
        pass

    def unsubscribe_subscriber_on_queue(self, queue_name: str) -> None:
        pass

    def resume_subscriber_on_queue(self, queue_name: str) -> None:
        pass

    def stop(self) -> None:
        pass
