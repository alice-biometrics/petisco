from abc import abstractmethod

from petisco.base.domain.message.command import Command
from petisco.base.domain.message.message_bus import MessageBus


class CommandBus(MessageBus):
    @abstractmethod
    def dispatch(self, command: Command):
        raise NotImplementedError

    def publish(self, command: Command):
        self.dispatch(command)

    def retry_publish_only_on_store_queue(self, command: Command):
        pass

    def _check_is_command(self, command: Command):
        if not command or not issubclass(command.__class__, Command):
            raise TypeError("CommandBus only publishes DomainEvent objects")

    @abstractmethod
    def close(self):
        raise NotImplementedError
