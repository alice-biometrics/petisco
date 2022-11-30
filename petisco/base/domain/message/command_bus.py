from abc import abstractmethod

from petisco.base.domain.message.command import Command
from petisco.base.domain.message.message_bus import MessageBus


class CommandBus(MessageBus[Command]):
    """
    A base class to implement an infrastructure-based bus to dispatch commands.
    """

    @abstractmethod
    def dispatch(self, command: Command) -> None:
        """
        Dispatch one Command
        """
        raise NotImplementedError

    def publish(self, command: Command) -> None:
        self.dispatch(command)

    def retry_publish_only_on_store_queue(self, command: Command) -> None:
        pass

    def _check_is_command(self, command: Command) -> None:
        if not command or not issubclass(command.__class__, Command):
            raise TypeError("CommandBus only publishes DomainEvent objects")

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
