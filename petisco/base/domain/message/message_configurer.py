from __future__ import annotations

from abc import abstractmethod

from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.base.misc.interface import Interface


class MessageConfigurer(Interface):
    @abstractmethod
    def configure_subscribers(
        self,
        subscribers: list[type[MessageSubscriber]],
        *,
        clear_subscriber_before: bool = False,
        clear_store_before: bool = False,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError
