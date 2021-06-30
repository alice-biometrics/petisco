import pytest

from petisco import Message


class MyMessage(Message):
    pass


@pytest.mark.unit
def test_message_should_create_message_input_and_output():
    message = MyMessage()

    message_json = message.json()

    retrieved_message = Message.from_json(message_json)

    assert message == retrieved_message
    assert id(message) != id(retrieved_message)


@pytest.mark.unit
def test_message_should_create_message_with_required_values():

    message = MyMessage()

    assert hasattr(message, "message_id")
    assert hasattr(message, "version")
    assert hasattr(message, "occurred_on")
    assert hasattr(message, "name")
    assert hasattr(message, "type")
    assert hasattr(message, "attributes")
    assert hasattr(message, "meta")


@pytest.mark.unit
def test_message_should_create_random_message_ids():

    message_1 = MyMessage()

    message_2 = MyMessage()

    assert message_1.message_id != message_2.message_id
    assert message_1.occurred_on != message_2.occurred_on
