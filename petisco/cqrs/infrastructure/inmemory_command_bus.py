from petisco.cqrs.domain.command import Command
from petisco.cqrs.domain.command_bus import CommandBus


class NoHandlerForMessageException(Exception):
    pass


class InMemoryCommandBus(CommandBus):
    def dispatch(self, command: Command):
        handler = self.command_handlers.get(command.name())
        if not handler:
            raise NoHandlerForMessageException(
                f"Not Handler defined for {command.name()}. Please, add it on the CommandBus initialization."
            )
        handler(command)
