import pytest

from petisco import Message


class MyMessage(Message):
    ...


@pytest.mark.unit
class TestMessage:
    def should_create_message_input_and_output(self):  # noqa
        message = Message()
        message_json = message.json()
        breakpoint()
        retrieved_message = Message.from_json(message_json)

        assert message == retrieved_message
        assert id(message) != id(retrieved_message)

    def should_create_message_with_required_values(self):  # noqa
        message = Message()

        assert hasattr(message, "message_id")
        assert hasattr(message, "version")
        assert hasattr(message, "occurred_on")
        assert hasattr(message, "name")
        assert hasattr(message, "type")
        assert hasattr(message, "attributes")
        assert hasattr(message, "meta")

    def should_create_random_message_ids(self):  # noqa
        message_1 = MyMessage()

        message_2 = MyMessage()

        assert message_1.message_id != message_2.message_id
        assert message_1.occurred_on != message_2.occurred_on

    def should_not_share_attributes_between_instances(self):  # noqa
        message_1 = MyMessage()
        message_1._set_attributes(foo="hola", bar="mundo")  # noqa

        message_2 = MyMessage()
        message_2._set_attributes(foo="hola2", bar="mundo2")  # noqa

        assert message_1.attributes["foo"] != message_2.attributes["foo"]
        assert message_1.attributes["bar"] != message_2.attributes["bar"]
