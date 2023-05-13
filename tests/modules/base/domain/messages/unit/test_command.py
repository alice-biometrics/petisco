import pytest

from petisco import Command


class MyCommand(Command):
    my_specific_value: str


@pytest.mark.unit
class TestCommand:
    def should_create_command_input_and_output(self):
        command = MyCommand(my_specific_value="whatever")

        command_json = command.json()

        retrieved_command = MyCommand.from_json(command_json)

        assert command.dict() == retrieved_command.dict()
        assert id(command) != id(retrieved_command)

    def should_create_command_input_and_output_with_specific_target_type(self):
        command = MyCommand(my_specific_value="whatever")

        command_json = command.json()

        retrieved_command = MyCommand.from_json(command_json, target_type=MyCommand)

        assert type(command) == type(retrieved_command)
        assert command.dict() == retrieved_command.dict()
        assert id(command) != id(retrieved_command)
        assert command.my_specific_value == retrieved_command.my_specific_value

    def should_create_command_with_required_values(self):

        command = MyCommand(my_specific_value="whatever")

        assert hasattr(command, "my_specific_value")
        assert hasattr(command, "attributes")
        assert getattr(command, "attributes") == {"my_specific_value": "whatever"}
        assert hasattr(command, "message_id")
        assert hasattr(command, "type")
        assert getattr(command, "type") == "command"
        assert hasattr(command, "version")
        assert hasattr(command, "occurred_on")
        assert hasattr(command, "name")
        assert hasattr(command, "meta")
