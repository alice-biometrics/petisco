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
        assert hasattr(command, "_message_attributes")
        assert getattr(command, "_message_attributes") == {
            "my_specific_value": "whatever"
        }
        assert hasattr(command, "_message_id")
        assert hasattr(command, "type")
        assert getattr(command, "type") == "command"
        assert hasattr(command, "_message_version")
        assert hasattr(command, "_message_occurred_on")
        assert hasattr(command, "_message_name")
        assert hasattr(command, "_message_meta")

    def should_create_command_with_correct_name_defined_inside_a_function(  # noqa
        self,
    ):
        class MyInnerCommand(Command):
            ...

        command = MyInnerCommand()
        assert command.get_message_name() == "my.inner.command"
