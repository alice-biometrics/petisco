import sys

import pytest
import validators

from petisco import InvalidUuid, Uuid


@pytest.mark.unit
class TestUuid:
    raw_uuid: str

    def setup_method(self):
        self.raw_uuid = "4E6660D7-B037-4C75-Adc8-272D62944Abb"

    def should_success_when_construct_and_serialize_with_inner_value(self):
        uuid = Uuid(value=self.raw_uuid)

        assert uuid.value == self.raw_uuid
        assert uuid.dict() == self.raw_uuid

    def should_success_when_construct_with_classmethod_and_serialize_with_inner_value(
        self,
    ):
        uuid = Uuid.from_value(self.raw_uuid)

        assert uuid.value == self.raw_uuid
        assert uuid.dict() == self.raw_uuid

    def should_success_when_generate_a_v4_version(self):
        uuid = Uuid.v4()
        assert isinstance(uuid, Uuid)
        assert validators.uuid(uuid.value)

    def should_success_when_equal_when_values_are_equals(self):
        uuid = Uuid.from_value(self.raw_uuid)
        other = Uuid.from_value(self.raw_uuid)

        assert uuid == other
        assert id(uuid) != id(other)

    def should_fail_when_values_are_not_equals(self):
        uuid = Uuid.from_value(self.raw_uuid)
        other = Uuid.from_value("33D42D79-1B22-40C9-8Cb5-7Ae88D3Ccc6A")

        assert uuid != other
        assert id(uuid) != id(other)

    def should_fail_when_input_is_not_a_valid_uuid(self):

        with pytest.raises(InvalidUuid) as excinfo:
            Uuid(value="non-uuid")

        assert "InvalidUuid (non-uuid)" in str(excinfo.value)

    def should_fail_when_input_is_not_a_valid_uuid_with_classmethod(self):

        with pytest.raises(InvalidUuid) as excinfo:
            Uuid.from_value("non-uuid")

        assert "InvalidUuid (non-uuid)" in str(excinfo.value)

    def should_return_an_object_of_a_child_class(self):
        class UserId(Uuid):
            pass

        type_hint = UserId.v4.__annotations__["return"]

        if sys.version_info < (3, 11):
            assert type_hint == "Uuid"
        else:
            assert type_hint == "UserId"
