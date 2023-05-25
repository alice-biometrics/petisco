from __future__ import annotations

from abc import abstractmethod

from meiga import BoolResult

from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_subscriber import MessageSubscriber


class AllMessageSubscriber(MessageSubscriber):
    def subscribed_to(self) -> list[type[Message]]:
        return [Message]

    @abstractmethod
    def handle(self, message: Message) -> BoolResult:
        raise NotImplementedError()
