from __future__ import annotations

import re
from abc import abstractmethod
from types import FunctionType
from typing import Any

from meiga import BoolResult

from petisco.base.application.middleware.middleware import Middleware
from petisco.base.domain.message.command_bus import CommandBus
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_subscriber_info import MessageSubscriberInfo
from petisco.base.domain.message.not_implemented_command_bus import (
    NotImplementedCommandBus,
)
from petisco.base.domain.message.not_implemented_domain_event_bus import (
    NotImplementedDomainEventBus,
)
from petisco.base.misc.interface import Interface
from petisco.base.misc.result_mapper import ResultMapper
from petisco.base.misc.wrapper import wrapper


class MetaMessageSubscriber(type, Interface):
    domain_event_bus: DomainEventBus = NotImplementedDomainEventBus()
    command_bus: CommandBus = NotImplementedCommandBus()
    middlewares: list[Middleware] = []
    use_global_middlewares: bool = True

    def __new__(mcs, name: str, bases: tuple[Any, ...], namespace: dict[str, Any]) -> MetaMessageSubscriber:
        config = namespace.get("Config")

        if "handle" not in namespace:
            raise NotImplementedError("Petisco MessageSubscriber must implement an handle method")

        mapper = ResultMapper()

        new_namespace = {}
        for attributeName, attribute in namespace.items():
            if isinstance(attribute, FunctionType) and attribute.__name__ == "handle":
                attribute = wrapper(attribute, name, config, mapper)
            new_namespace[attributeName] = attribute

        return super().__new__(mcs, name, bases, new_namespace)

    @abstractmethod
    def subscribed_to(self) -> list[type[Message]]:
        raise NotImplementedError()

    @abstractmethod
    def handle(self, message: Message) -> BoolResult:
        raise NotImplementedError()


class MessageSubscriber(metaclass=MetaMessageSubscriber):
    @abstractmethod
    def subscribed_to(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def handle(self, message: Any) -> BoolResult:
        raise NotImplementedError()

    @classmethod
    def __repr__(cls) -> str:
        subscriptions = cls.subscribed_to(cls)  # type: ignore
        if not isinstance(subscriptions, list):
            subscriptions = [subscriptions]
        return f"{cls.__name__}: subscribed_to {[class_type.__name__ for class_type in subscriptions]}"

    def set_domain_event_bus(self, domain_event_bus: DomainEventBus) -> None:
        self.domain_event_bus = domain_event_bus

    def set_command_bus(self, command_bus: CommandBus) -> None:
        self.command_bus = command_bus

    def get_subscriber_name(self) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__class__.__name__).lower()

    def get_message_subscribers_info(self) -> list[MessageSubscriberInfo]:
        subscribers_info = []
        for class_type in self.subscribed_to():
            subscribers_info.append(MessageSubscriberInfo.from_class_type(class_type))
        return subscribers_info
