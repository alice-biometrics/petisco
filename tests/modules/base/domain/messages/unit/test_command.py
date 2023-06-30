from datetime import datetime

import pytest

from petisco import Command, Uuid
from tests.modules.base.domain.messages.unit.commands import (
    AttributesCommand,
    MostConflictingCommand,
    MyCommand,
    NameConflictCommand,
    NoAttributesCommand,
    VersionConflictCommand,
)

COMMANDS = [
    NoAttributesCommand(),
    AttributesCommand(id=Uuid.v4().value, username="whatever"),
    NameConflictCommand(name="whatever"),
    VersionConflictCommand(version=100),
]


@pytest.mark.unit
class TestCommand:
    @pytest.mark.parametrize("command", COMMANDS)
    def should_create_command_input_and_output(self, command: Command):  # noqa
        command_json = command.json()

        retrieved_command = MyCommand.from_json(command_json)

        assert command.dict() == retrieved_command.dict()
        assert id(command) != id(retrieved_command)

    def should_create_command_input_and_output_with_specific_target_type(self):  # noqa
        command = MyCommand(my_specific_value="whatever")

        command_json = command.json()

        retrieved_command = MyCommand.from_json(command_json, target_type=MyCommand)

        assert type(command) == type(retrieved_command)
        assert command.dict() == retrieved_command.dict()
        assert id(command) != id(retrieved_command)
        assert command.my_specific_value == retrieved_command.my_specific_value

    def should_create_command_with_required_values(self):  # noqa
        command = MyCommand(my_specific_value="whatever")

        assert hasattr(command, "my_specific_value")
        assert hasattr(command, "_message_attributes")
        assert getattr(command, "_message_attributes") == {
            "my_specific_value": "whatever"
        }
        assert hasattr(command, "_message_id")
        assert hasattr(command, "_message_type")
        assert getattr(command, "_message_type") == "command"
        assert hasattr(command, "_message_version")
        assert hasattr(command, "_message_occurred_on")
        assert hasattr(command, "_message_name")
        assert hasattr(command, "_message_meta")

    def should_create_command_and_keep_message_version_when_exist_a_message_attribute(  # noqa
        self,
    ):
        expected_message_version = 2

        domain_event = VersionConflictCommand(version=100)
        domain_event_json = domain_event.json()
        retrieved_domain_event = Command.from_json(domain_event_json)

        assert domain_event.get_message_version() == expected_message_version
        assert retrieved_domain_event.get_message_version() == expected_message_version

    def should_create_command_and_keep_message_name_when_exist_a_message_attribute(  # noqa
        self,
    ):
        domain_event = NameConflictCommand(name="whatever")
        domain_event_json = domain_event.json()
        retrieved_domain_event = Command.from_json(domain_event_json)
        assert domain_event.get_message_name() == "name.conflict.command"
        assert retrieved_domain_event.get_message_name() == "name.conflict.command"

    def should_create_command_with_most_conflicting_domain_event(  # noqa
        self,
    ):
        now = datetime.utcnow()
        command = MostConflictingCommand(
            name="given-name",
            version=2,
            occurred_on=now,
            attributes={"other-attribute": True},
            meta={"client_id": "acme"},
            type="given-type",
        )
        assert command.get_message_name() == "most.conflicting.command"
        assert command.get_message_version() == 2
        assert command.get_message_occurred_on() != now
        assert command.get_message_attributes() == {
            "name": "given-name",
            "version": 2,
            "occurred_on": now,
            "attributes": {"other-attribute": True},
            "meta": {"client_id": "acme"},
            "type": "given-type",
        }
        assert command.get_message_meta() == {}

    def should_create_command_with_correct_name_defined_inside_a_function(  # noqa
        self,
    ):
        class MyInnerCommand(Command):
            ...

        command = MyInnerCommand()
        assert command.get_message_name() == "my.inner.command"
