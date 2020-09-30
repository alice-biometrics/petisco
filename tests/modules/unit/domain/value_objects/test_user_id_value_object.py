import pytest
from meiga import Success
from meiga.assertions import assert_failure, assert_success
from meiga.decorators import meiga

from petisco.domain.value_objects.user_id import UserId
from petisco.domain.errors.length_limit_string_value_object_error import (
    ExceedLengthLimitValueObjectError,
)


@pytest.mark.unit
def test_should_declare_a_user_id_manually():

    value = "my_user_id"
    user_id = UserId(value)

    assert isinstance(user_id, UserId)
    assert user_id.value == value


@pytest.mark.unit
def test_should_declare_a_user_id_with_empty_string():
    value = ""
    user_id = UserId(value)
    assert isinstance(user_id, UserId)
    assert user_id.value == value


@pytest.mark.unit
def test_should_declare_a_user_id_generated_automatically():
    user_id = UserId.generate()

    assert isinstance(user_id, UserId)
    assert len(user_id.value) == 16


@pytest.mark.unit
def test_should_fail_when_declare_a_user_id_that_exceeds_default_length_limits():
    with pytest.raises(ExceedLengthLimitValueObjectError):
        UserId("my_user_id_is_too_long_for_default_limit_length")


@pytest.mark.unit
def test_should_return_success_user_id_if_generate_user_id_on_meiga_decorated_method():
    @meiga
    def controller():
        return Success(UserId.generate())

    result = controller()
    assert_success(result, value_is_instance_of=UserId)


@pytest.mark.unit
def test_should_fail_when_declare_a_non_valid_user_id():
    @meiga
    def controller():
        user_id = UserId("my_user_id_is_too_long_for_default_limit_length")
        return Success(user_id)

    result = controller()
    assert_failure(result, value_is_instance_of=ExceedLengthLimitValueObjectError)
