from __future__ import annotations

from abc import abstractmethod

from petisco.base.domain.message.command import Command
from petisco.base.domain.message.message_bus import MessageBus


class CommandBus(MessageBus[Command]):
    """
    A base class to implement an infrastructure-based bus to dispatch commands.
    """

    @abstractmethod
    def dispatch(self, command: Command | list[Command]) -> None:
        """
        Dispatch one Command or a list of commands

        Dispatch several commands could be a code smell but some use case could require this feature.
        """
        raise NotImplementedError

    def publish(self, command: Command | list[Command]) -> None:
        self.dispatch(command)

    def _check_is_command(self, command: Command) -> None:
        if not command or not issubclass(command.__class__, Command):
            raise TypeError(f"{self.__class__.__name__} only publishes Command objects")

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
