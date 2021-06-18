from typing import List
from abc import abstractmethod

from petisco.base.domain.message.message_subscriber import MessageSubscriber
from petisco.base.util.interface import Interface
from petisco.base.domain.message.message import Message


class MessageConfigurer(Interface):
    @abstractmethod
    def configure_subscribers(self, subscribers: List[MessageSubscriber]):
        raise NotImplementedError

    @abstractmethod
    def configure_message(self, message: Message):
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        raise NotImplementedError
