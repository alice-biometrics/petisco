from abc import abstractmethod
from typing import List

from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.base.misc.interface import Interface


class MessageConfigurer(Interface):
    @abstractmethod
    def configure_subscribers(self, subscribers: List[MessageSubscriber]):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError
