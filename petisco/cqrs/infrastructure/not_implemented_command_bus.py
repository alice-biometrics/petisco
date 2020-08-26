from petisco.cqrs.domain.command import Command
from petisco.cqrs.domain.command_bus import CommandBus


class NotImplementedCommandBus(CommandBus):
    def dispatch(self, command: Command):
        pass
