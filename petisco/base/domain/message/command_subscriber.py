from __future__ import annotations

from abc import abstractmethod

from meiga import BoolResult

from petisco.base.domain.message.command import Command
from petisco.base.domain.message.message_subscriber import MessageSubscriber

# Unlike in the domain event subscriber,
# in the command handler the command -> command handler
# relationship is 1 to 1 and that is why we use Type[Command] instead of List[Type[Command]]
# and overwrite get_message_subscribers_info base method
from petisco.base.domain.message.message_subscriber_info import MessageSubscriberInfo


class CommandSubscriber(MessageSubscriber):
    """
    A base class to model your command subscribers (or also called CommandHandlers).
    Inherit from this class to parser the command, configure middlewares and instantiate and execute a UseCase.
    """

    @abstractmethod
    def subscribed_to(self) -> type[Command]:
        raise NotImplementedError()

    @abstractmethod
    def handle(self, command: Command) -> BoolResult:
        raise NotImplementedError()

    def get_message_subscribers_info(self) -> list[MessageSubscriberInfo]:
        return [MessageSubscriberInfo.from_class_type(self.subscribed_to())]
