import pytest

from petisco import Command


class MyCommand(Command):
    name: str


@pytest.mark.unit
def test_command_should_create_command_input_and_output():
    command = MyCommand(name="whatever")

    command_json = command.json()

    retrieved_command = MyCommand.from_json(command_json)

    assert command.dict() == retrieved_command.dict()
    assert id(command) != id(retrieved_command)


@pytest.mark.unit
def test_command_should_create_command_input_and_output_with_specific_target_type():
    command = MyCommand(name="whatever")

    command_json = command.json()

    retrieved_command = MyCommand.from_json(command_json, target_type=MyCommand)

    assert type(command) == type(retrieved_command)
    assert command.dict() == retrieved_command.dict()
    assert id(command) != id(retrieved_command)


@pytest.mark.unit
def test_command_should_create_command_with_required_values():

    command = MyCommand(name="whatever")

    assert hasattr(command, "attributes")
    assert getattr(command, "attributes") == {"name": "whatever"}
    assert hasattr(command, "message_id")
    assert hasattr(command, "type")
    assert getattr(command, "type") == "command"
    assert hasattr(command, "version")
    assert hasattr(command, "occurred_on")
    assert hasattr(command, "name")
    assert hasattr(command, "meta")