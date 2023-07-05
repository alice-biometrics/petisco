import pytest

from petisco.base.domain.message.legacy_message import LegacyMessage


class MyMessage(LegacyMessage):
    ...


@pytest.mark.unit
class TestLegacyMessage:
    def should_create_message_input_and_output(self):  # noqa
        message = LegacyMessage()
        message_json = message.json()
        retrieved_message = LegacyMessage.from_json(message_json)
        assert message == retrieved_message
        assert id(message) != id(retrieved_message)
        assert retrieved_message._message_type == "message"

    def should_create_message_with_required_values(self):  # noqa
        message = LegacyMessage()

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
        message_1 = MyMessage()
        message_1._set_attributes(foo="hola", bar="mundo")  # noqa

        message_2 = MyMessage()
        message_2._set_attributes(foo="hola2", bar="mundo2")  # noqa

        assert (
            message_1.get_message_attributes()["foo"]
            != message_2.get_message_attributes()["foo"]
        )
        assert (
            message_1.get_message_attributes()["bar"]
            != message_2.get_message_attributes()["bar"]
        )
