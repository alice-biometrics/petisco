import pytest
import validators
from pydantic import field_validator

from petisco import InvalidUuid, LegacyUuid


class TaskId(LegacyUuid):
    @field_validator("value")
    def validate_value(cls, value):
        if value is None or not validators.uuid(value) and (value is None or len(value) != 28):
            raise InvalidUuid(uuid_value=value)
        return value


@pytest.mark.unit
def test_uuid_inheritance_should_success_when_construct_and_serialize_with_inner_value():
    task_id = TaskId(value="4e6660d7-b037-4c75-adc8-272d62944abb")

    assert task_id.value == "4e6660d7-b037-4c75-adc8-272d62944abb"
    assert task_id.model_dump() == "4e6660d7-b037-4c75-adc8-272d62944abb"


@pytest.mark.unit
def test_uuid_inheritance_should_success_when_use_a_legacy_value_allowed_in_specific_validator():
    task_id = TaskId(value="SFHem4THDVnNNQjL447Phieh4rst")

    assert task_id.value == "SFHem4THDVnNNQjL447Phieh4rst"
    assert task_id.model_dump() == "SFHem4THDVnNNQjL447Phieh4rst"


@pytest.mark.unit
def test_uuid_inheritance_should_fail_when_input_is_not_a_valid_uuid():
    with pytest.raises(InvalidUuid) as excinfo:
        TaskId(value="non-uuid")

    assert "InvalidUuid (non-uuid)" in str(excinfo.value)


@pytest.mark.unit
def test_uuid_inheritance__should_fail_when_input_is_not_a_valid_uuid_with_classmethod():
    with pytest.raises(InvalidUuid) as excinfo:
        TaskId("non-uuid")

    assert "InvalidUuid (non-uuid)" in str(excinfo.value)


#
# @pytest.mark.unit
# def test_uuid_should_success_when_construct_with_classmethod_and_serialize_with_inner_value():
#
#     uuid = Uuid.from_value("4E6660D7-B037-4C75-Adc8-272D62944Abb")
#
#     assert uuid.value == "4E6660D7-B037-4C75-Adc8-272D62944Abb"
#     assert uuid.dict() == "4E6660D7-B037-4C75-Adc8-272D62944Abb"
#
#
# @pytest.mark.unit
# def test_uuid_should_success_when_generate_a_v4_version():
#
#     uuid = Uuid.v4()
#
#     assert validators.uuid(uuid.value)
#
#
# @pytest.mark.unit
# def test_uuid_should_success_when_equal_when_values_are_equals():
#
#     uuid = Uuid.from_value("4E6660D7-B037-4C75-Adc8-272D62944Abb")
#     other = Uuid.from_value("4E6660D7-B037-4C75-Adc8-272D62944Abb")
#
#     assert uuid == other
#     assert id(uuid) != id(other)
#
#
# @pytest.mark.unit
# def test_uuid_should_fail_when_values_are_not_equals():
#
#     uuid = Uuid.from_value("4E6660D7-B037-4C75-Adc8-272D62944Abb")
#     other = Uuid.from_value("43D42D79-1B22-40C9-8Cb5-7Ae88D3Ccc6A")
#
#     assert uuid != other
#     assert id(uuid) != id(other)
#
#
# @pytest.mark.unit
# def test_uuid_should_fail_when_input_is_not_a_valid_uuid():
#
#     with pytest.raises(InvalidUuid) as excinfo:
#         Uuid(value="non-uuid")
#
#     assert "Invalid Uuid (non-uuid)" in str(excinfo.value)
#
#
# @pytest.mark.unit
# def test_uuid_should_fail_when_input_is_not_a_valid_uuid_with_classmethod():
#
#     with pytest.raises(InvalidUuid) as excinfo:
#         Uuid.from_value("non-uuid")
#
#     assert "Invalid Uuid (non-uuid)" in str(excinfo.value)
#
