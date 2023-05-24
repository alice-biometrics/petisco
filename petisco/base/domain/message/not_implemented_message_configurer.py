from __future__ import annotations

from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.base.domain.message.message_subscriber import MessageSubscriber


class NotImplementedMessageConfigurer(MessageConfigurer):
    def configure_subscribers(
        self,
        subscribers: list[MessageSubscriber],
        clear_subscriber_before: bool = False,
        clear_store_before: bool = False,
    ) -> None:
        pass

    def clear(self) -> None:
        pass
