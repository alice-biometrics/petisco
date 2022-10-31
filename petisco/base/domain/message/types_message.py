from typing import TypeVar, Union

from petisco.base.domain.message.command import Command
from petisco.base.domain.message.domain_event import DomainEvent
from petisco.base.domain.message.message import Message

TypeMessage = TypeVar("TypeMessage", bound=Message)

AnyMessage = Union[Message, DomainEvent, Command]
