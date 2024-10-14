from datetime import timezone

import pytest
from pydantic.main import BaseModel

from petisco import Message
from tests.modules.base.mothers.message_mother import MessageMother


class MyMessage(Message): ...


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
        assert message_1.get_message_occurred_on() != message_2.get_message_occurred_on()

    def should_not_share_attributes_between_instances(self):  # noqa
        message_1 = MyMessageWithAttributes(foo="hola", bar="mundo")

        message_2 = MyMessageWithAttributes(foo="hola2", bar="mundo2")

        assert message_1.get_message_attributes()["foo"] != message_2.get_message_attributes()["foo"]
        assert message_1.get_message_attributes()["bar"] != message_2.get_message_attributes()["bar"]

    def should_check_ocurred_on_datetime_has_timezone(self):  # noqa
        message = Message()

        occurred_on = message.get_message_occurred_on()

        assert occurred_on.tzinfo == timezone.utc

    def should_check_ocurred_on_datetime_has_timezone_when_format_and_from_format(
        self,
    ):  # noqa
        message = Message()

        message_json = message.format_json()
        retrieved_message = Message.from_format(message_json)

        occurred_on = message.get_message_occurred_on()
        retrieved_occurred_on = retrieved_message.get_message_occurred_on()

        assert occurred_on.tzinfo == timezone.utc
        assert retrieved_occurred_on.tzinfo == timezone.utc

        assert message == retrieved_message
        assert id(message) != id(retrieved_message)
        assert occurred_on == retrieved_occurred_on

    def should_check_ocurred_on_datetime_has_timezone_when_is_old_format(self):  # noqa
        message_json_with_occurred_on_without_timezone = '{"data": {"id": "69d71598-4920-4a59-b006-e4caa3316932", "type": "message", "type_message": "message", "version": 1, "occurred_on": "2023-09-20 10:09:57.220432", "attributes": {}, "meta": {}}}'

        retrieved_message = Message.from_format(message_json_with_occurred_on_without_timezone)
        retrieved_occurred_on = retrieved_message.get_message_occurred_on()

        assert retrieved_occurred_on.tzinfo == timezone.utc

    def should_share_same_hash_when_same_message(self):  # noqa
        message_1 = MessageMother.any()
        message_2 = Message.from_format(message_1.format())

        assert hash(message_1) == hash(message_2)

    def should_have_different_hash_when_different_message(self):  # noqa
        message_1 = MessageMother.any()
        message_2 = MessageMother.other()

        assert hash(message_1) != hash(message_2)

    def should_set_a_list_to_messages_to_keep_unique_values(self):  # noqa
        message_1 = MessageMother.any()
        message_2 = Message.from_format(message_1.format())
        messages = [
            message_1,
            message_2,
            MessageMother.other("other_1"),
            MessageMother.other("other_2"),
            MessageMother.other("other_3"),
        ]

        unique_messages = list(set(messages))

        assert len(messages) == 5
        assert len(unique_messages) == 4

    def should_format_message_with_base_model(self):
        class Model(BaseModel):
            model_att: str

        message = Message()
        message._message_attributes = {"base_model": Model(model_att="att")}

        message_json = message.format_json()
        retrieved_message = Message.from_format(message_json)

        assert message == retrieved_message

