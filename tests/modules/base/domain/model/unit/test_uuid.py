import pytest
import validators
from pydantic import BaseModel

from petisco import InvalidUuid, Uuid


@pytest.mark.unit
class TestUuid:
    def should_success_when_construct_and_serialize_with_inner_value(self):  # noqa
        uuid = Uuid("4e6660d7-b037-4c75-adc8-272d62944abb")

        assert uuid.value == "4e6660d7-b037-4c75-adc8-272d62944abb"

    def should_success_when_construct_with_classmethod_and_serialize_with_inner_value(
        self,
    ):  # noqa
        uuid = Uuid("4e6660d7-b037-4c75-adc8-272d62944abb")

        assert uuid.value == "4e6660d7-b037-4c75-adc8-272d62944abb"

    def should_success_when_generate_a_v4_version(self):  # noqa
        uuid = Uuid.v4()

        assert isinstance(uuid, Uuid)
        assert validators.uuid(uuid.value)

    def should_success_when_equal_when_values_are_equals(self):  # noqa
        uuid = Uuid("4e6660d7-b037-4c75-adc8-272d62944abb")
        other = Uuid("4e6660d7-b037-4c75-adc8-272d62944abb")

        assert uuid == other
        assert id(uuid) != id(other)

    def should_fail_when_values_are_not_equals(self):  # noqa
        uuid = Uuid("4e6660d7-b037-4c75-adc8-272d62944abb")
        other = Uuid("d0f93ded-4dda-44ff-b3a2-9a590cdb8e4d")

        assert uuid != other
        assert id(uuid) != id(other)

    def should_fail_when_input_is_not_a_valid_uuid(self):  # noqa
        with pytest.raises(InvalidUuid) as excinfo:
            Uuid(value="non-uuid")

        assert "InvalidUuid (non-uuid)" in str(excinfo.value)

    def should_fail_when_input_is_not_a_valid_uuid_with_classmethod(self):  # noqa
        with pytest.raises(InvalidUuid) as excinfo:
            Uuid("non-uuid")

        assert "InvalidUuid (non-uuid)" in str(excinfo.value)

    def should_v4_return_an_object_of_a_child_class(self):  # noqa
        class UserId(Uuid):
            pass

        user_id = UserId.v4()

        assert isinstance(user_id, UserId)

    def should_success_when_construct_from_str(self):  # noqa
        uuid = Uuid("4e6660d7-b037-4c75-adc8-272d62944abb")

        assert uuid.value == "4e6660d7-b037-4c75-adc8-272d62944abb"

    def should_compare_without_using_value_property(self):  # noqa
        class UserId(Uuid):
            pass

        user_id = UserId.v4()

        assert isinstance(user_id, UserId)
        assert user_id == user_id.value

    def should_success_when_init_from_uuid(self):  # noqa
        first_uuid = Uuid.v4()
        uuid = Uuid(first_uuid)

        assert isinstance(uuid, Uuid)
        assert uuid == first_uuid

    def should_success_when_used_in_a_base_model(self):  # noqa
        class User(BaseModel):
            id: Uuid

        first_uuid = Uuid.v4()
        user = User(id=first_uuid)

        assert isinstance(user, User)
        assert isinstance(user.id, Uuid)
