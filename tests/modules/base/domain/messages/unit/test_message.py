import pytest

from petisco import Message


class MyMessage(Message):
    ...


class MyMessageWithAttributes(Message):
    foo: str
    bar: str


@pytest.mark.unit
class TestMessage:
    def should_create_message_input_and_output(self):  # noqa
        message = Message()
        message_json = message.format_json()
        retrieved_message = Message.from_format(message_json)
        assert message == retrieved_message
        assert id(message) != id(retrieved_message)

    def should_create_message_with_required_values(self):  # noqa
        message = Message()

        assert hasattr(message, "_message_id")
        assert hasattr(message, "_message_version")
        assert hasattr(message, "_message_occurred_on")
        assert hasattr(message, "_message_name")
        assert hasattr(message, "_message_type")
        assert hasattr(message, "_message_attributes")
        assert hasattr(message, "_message_meta")

    def should_create_random_message_ids(self):  # noqa
        message_1 = MyMessage()

        message_2 = MyMessage()

        assert message_1.get_message_id() != message_2.get_message_id()
        assert (
            message_1.get_message_occurred_on() != message_2.get_message_occurred_on()
        )

    def should_not_share_attributes_between_instances(self):  # noqa
        message_1 = MyMessageWithAttributes(foo="hola", bar="mundo")

        message_2 = MyMessageWithAttributes(foo="hola2", bar="mundo2")

        assert (
            message_1.get_message_attributes()["foo"]
            != message_2.get_message_attributes()["foo"]
        )
        assert (
            message_1.get_message_attributes()["bar"]
            != message_2.get_message_attributes()["bar"]
        )

    def should_check_timestamp_from_ocurred_on_datetime(self):  # noqa
        message = Message()

        original_timestamp = message.get_message_occurred_on().timestamp()

        message_json = message.format_json()
        retrieved_message = Message.from_format(message_json)

        retrieved_timestamp = message.get_message_occurred_on().timestamp()

        assert message == retrieved_message
        assert id(message) != id(retrieved_message)
        assert original_timestamp == retrieved_timestamp
