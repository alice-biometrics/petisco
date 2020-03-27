import pytest
from meiga import Success
from meiga.assertions import assert_failure, assert_success
from meiga.decorators import meiga

from petisco.domain.value_objects.user_id import UserId
from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)


@pytest.mark.unit
def test_should_declare_a_user_id_manually():
    user_id = UserId("my_user_id")

    assert_success(
        user_id.to_result(), value_is_instance_of=str, value_is_equal_to="my_user_id"
    )


@pytest.mark.unit
def test_should_declare_a_user_id_with_empty_string():
    user_id = UserId("")

    assert_success(user_id.to_result(), value_is_instance_of=str, value_is_equal_to="")


@pytest.mark.unit
def test_should_declare_a_user_id_generated_automatically():
    user_id = UserId.generate()

    assert_success(user_id.to_result(), value_is_instance_of=str)
    assert len(user_id.to_result().value) == 16


@pytest.mark.unit
def test_should_faile_when_declare_a_user_id_that_exceeds_default_length_limits():
    user_id = UserId("my_user_id_is_too_long_for_default_limit_length")

    assert_failure(
        user_id.to_result(), value_is_instance_of=InputExceedLengthLimitError
    )


@pytest.mark.unit
def test_should_declare_a_user_id_call_to_result_and_try_to_unwrap_or_return():
    @meiga
    def controller():
        user_id = UserId.generate().to_result().unwrap_or_return()
        return Success(user_id)

    result = controller()
    assert_success(result, value_is_instance_of=UserId)


@pytest.mark.unit
def test_should_fail_when_declare_a_non_valid_user_id_and_call_to_result_and_try_to_unwrap_or_return():
    @meiga
    def controller():
        user_id = (
            UserId("my_user_id_is_too_long_for_default_limit_length")
            .to_result()
            .unwrap_or_return()
        )
        return Success(user_id)

    result = controller()
    assert_failure(result, value_is_instance_of=InputExceedLengthLimitError)


@pytest.mark.unit
def test_should_declare_a_user_id_call_guard():
    @meiga
    def controller():
        user_id = UserId.generate().guard()
        return Success(user_id)

    result = controller()
    assert_success(result, value_is_instance_of=UserId)


@pytest.mark.unit
def test_should_fail_when_declare_a_non_valid_user_id_call_guard():
    @meiga
    def controller():
        user_id = UserId("my_user_id_is_too_long_for_default_limit_length").guard()
        return Success(user_id)

    result = controller()
    assert_failure(result, value_is_instance_of=InputExceedLengthLimitError)
