import pytest
from meiga import Success
from meiga.assertions import assert_failure, assert_success
from meiga.decorators import meiga

from petisco.domain.value_objects.user_id import UserId
from petisco.domain.value_objects.uuid import InvalidUuidError


@pytest.mark.unit
@pytest.mark.parametrize(
    "value", ["0VAnhfnTtMJk3SBN", "9f74b5c0-2196-4a27-a03f-cb92d66e2bbd"]
)
def test_should_declare_a_user_id_manually(value):

    user_id = UserId(value)

    assert isinstance(user_id, UserId)
    assert user_id.value == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "value", ["user_id", "my_user_id_is_too_long_for_default_limit_length"]
)
def test_should_fail_user_id_when_declare_a_non_valid_user_id(value):
    @meiga
    def controller():
        user_id = UserId(value)
        return Success(user_id)

    result = controller()
    assert_failure(result, value_is_instance_of=InvalidUuidError)


@pytest.mark.unit
def test_should_declare_a_user_id_with_empty_string():
    with pytest.raises(InvalidUuidError):
        UserId("")


@pytest.mark.unit
def test_should_declare_a_user_id_with_none():
    with pytest.raises(InvalidUuidError):
        UserId(None)


@pytest.mark.unit
def test_should_declare_a_user_id_generated_automatically():
    user_id = UserId.generate()

    assert isinstance(user_id, UserId)
    assert len(user_id.value) == 36


@pytest.mark.unit
def test_should_declare_a_legacy_user_id_generated_automatically():
    user_id = UserId.generate_legacy()

    assert isinstance(user_id, UserId)
    assert len(user_id.value) == 16


@pytest.mark.unit
def test_should_fail_when_declare_a_user_id_that_exceeds_default_length_limits():
    with pytest.raises(InvalidUuidError):
        UserId("my_user_id_is_too_long_for_default_limit_length")


@pytest.mark.unit
def test_should_return_success_user_id_if_generate_user_id_on_meiga_decorated_method():
    @meiga
    def controller():
        return Success(UserId.generate())

    result = controller()
    assert_success(result, value_is_instance_of=UserId)
