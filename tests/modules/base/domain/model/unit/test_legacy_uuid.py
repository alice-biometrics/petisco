from uuid import uuid4

import pytest
import validators

from petisco import InvalidUuid, LegacyUuid


@pytest.mark.unit
class TestLegacyUuid:
    def should_success_when_construct_and_serialize_with_inner_value(self):  # noqa
        uuid = LegacyUuid(value="4E6660D7-B037-4C75-Adc8-272D62944Abb")

        assert uuid.value == "4E6660D7-B037-4C75-Adc8-272D62944Abb"
        assert uuid.model_dump() == "4E6660D7-B037-4C75-Adc8-272D62944Abb"

    def should_success_when_construct_with_classmethod_and_serialize_with_inner_value(
        self,
    ):  # noqa
        uuid = LegacyUuid.from_value("4E6660D7-B037-4C75-Adc8-272D62944Abb")

        assert uuid.value == "4E6660D7-B037-4C75-Adc8-272D62944Abb"
        assert uuid.model_dump() == "4E6660D7-B037-4C75-Adc8-272D62944Abb"

    def should_success_when_generate_a_v4_version(self):  # noqa
        uuid = LegacyUuid.v4()

        assert isinstance(uuid, LegacyUuid)
        assert validators.uuid(uuid.value)

    def should_success_when_equal_when_values_are_equals(self):  # noqa
        uuid = LegacyUuid.from_value("4E6660D7-B037-4C75-Adc8-272D62944Abb")
        other = LegacyUuid.from_value("4E6660D7-B037-4C75-Adc8-272D62944Abb")

        assert uuid == other
        assert id(uuid) != id(other)

    def should_fail_when_values_are_not_equals(self):  # noqa
        uuid = LegacyUuid.from_value("4E6660D7-B037-4C75-Adc8-272D62944Abb")
        other = LegacyUuid.from_value("43D42D79-1B22-40C9-8Cb5-7Ae88D3Ccc6A")

        assert uuid != other
        assert id(uuid) != id(other)

    def should_fail_when_input_is_not_a_valid_uuid(self):  # noqa
        with pytest.raises(InvalidUuid) as excinfo:
            LegacyUuid(value="non-uuid")

        assert "InvalidUuid (non-uuid)" in str(excinfo.value)

    def should_fail_when_input_is_not_a_valid_uuid_with_classmethod(self):  # noqa
        with pytest.raises(InvalidUuid) as excinfo:
            LegacyUuid.from_value("non-uuid")

        assert "InvalidUuid (non-uuid)" in str(excinfo.value)

    def should_v4_return_an_object_of_a_child_class(self):  # noqa
        class UserId(LegacyUuid):
            pass

        user_id = UserId.v4()

        assert isinstance(user_id, UserId)

    def should_success_when_construct_from_uuid(self):  # noqa
        uuid_input = uuid4()

        uuid = LegacyUuid.from_uuid(uuid_input)

        assert uuid.value == str(uuid_input)
        assert uuid.model_dump() == str(uuid_input)

    def should_success_when_construct_from_str(self):  # noqa
        uuid = LegacyUuid.from_str("4E6660D7-B037-4C75-Adc8-272D62944Abb")

        assert uuid.value == "4E6660D7-B037-4C75-Adc8-272D62944Abb"
        assert uuid.model_dump() == "4E6660D7-B037-4C75-Adc8-272D62944Abb"

    def should_success_when_to_uuid(self):  # noqa
        raw_uuid = uuid4()

        uuid = LegacyUuid.from_uuid(raw_uuid)

        assert uuid.to_uuid() == raw_uuid
