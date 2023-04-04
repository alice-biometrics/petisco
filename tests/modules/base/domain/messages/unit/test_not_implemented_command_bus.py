from __future__ import annotations

import pytest

from petisco import Command, NotImplementedCommandBus
from tests.modules.extra.rabbitmq.mother.command_persist_user_mother import (
    CommandPersistUserMother,
)


@pytest.mark.unit
class TestNotImplementedCommandBus:
    @pytest.mark.parametrize("command", [CommandPersistUserMother.random()])
    def should_success_on_publish_a_domain_event(
        self, command: Command | list[Command]
    ):
        bus = NotImplementedCommandBus()
        bus.dispatch(command)

    def should_raise_an_exception_when_input_is_not_valid(self):
        bus = NotImplementedCommandBus()

        with pytest.raises(
            TypeError, match="NotImplementedCommandBus only publishes Command objects"
        ):
            bus.dispatch("invalid_input")
