from typing import TypeVar, Union

from petisco.base.domain.message.command import Command
from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_bus import MessageBus

TypeMessage = TypeVar("TypeMessage", bound=Message)
TypeMessageBus = TypeVar("TypeMessageBus", bound=MessageBus)


AnyMessage = Union[Message, DomainEvent, Command]
