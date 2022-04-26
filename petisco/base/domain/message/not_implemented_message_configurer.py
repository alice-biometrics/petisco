from typing import List

from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.base.domain.message.message_subscriber import MessageSubscriber


class NotImplementedMessageConfigurer(MessageConfigurer):
    def configure_subscribers(
        self, subscribers: List[MessageSubscriber], clear_before: bool = False
    ):
        pass

    def clear(self):
        pass
