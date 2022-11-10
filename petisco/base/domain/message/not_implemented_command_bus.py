from typing import List

from petisco.base.domain.message.command import Command
from petisco.base.domain.message.command_bus import CommandBus


class NotImplementedCommandBus(CommandBus):
    def dispatch(self, command: Command) -> None:
        self._check_is_command(command)
        meta = self.get_configured_meta()
        _ = command.update_meta(meta)

    def dispatch_list(self, commands: List[Command]) -> None:
        for command in commands:
            self._check_is_command(command)
            meta = self.get_configured_meta()
            _ = command.update_meta(meta)

    def close(self) -> None:
        pass
