import re
from abc import abstractmethod
from typing import List, Type

from meiga import BoolResult

from petisco.base.domain.message.message_bus import MessageBus
from petisco.base.domain.message.not_implemented_message_bus import (
    NotImplementedMessageBus,
)
from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_subscriber_info import MessageSubscriberInfo
from petisco.base.util.interface import Interface


class MessageSubscriber(Interface):
    def __init__(
        self,
        domain_event_bus: MessageBus = NotImplementedMessageBus(),
        command_bus: MessageBus = NotImplementedMessageBus(),
    ):
        self.domain_event_bus = domain_event_bus
        self.command_bus = command_bus

    @abstractmethod
    def subscribed_to(self) -> List[Type[Message]]:
        raise NotImplementedError()

    @abstractmethod
    def handle(self, message: Message) -> BoolResult:
        raise NotImplementedError()

    def get_subscriber_name(self) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()

    def get_message_subscribers_info(self) -> List[MessageSubscriberInfo]:
        subscribers_info = []
        for class_type in self.subscribed_to():
            subscribers_info.append(MessageSubscriberInfo.from_class_type(class_type))
        return subscribers_info

    @classmethod
    def __repr__(cls):
        subscriptions = cls.subscribed_to(cls)
        if not isinstance(subscriptions, list):
            subscriptions = [subscriptions]
        return f"{cls.__name__}: subscribed_to {[class_type.__name__ for class_type in subscriptions]}"
