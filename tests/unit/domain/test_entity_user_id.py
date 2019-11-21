import pytest
from meiga.assertions import assert_failure, assert_success

from petisco.domain.entities.user_id import UserId
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
def test_should_declare_a_user_id_generated_automatically():

    user_id = UserId.generate()

    assert_success(user_id.to_result(), value_is_instance_of=str)
    assert len(user_id.to_result().value) == 12


@pytest.mark.unit
def test_should_declare_a_user_id_that_exceeds_default_length_limits():

    user_id = UserId("my_user_id_is_too_long_for_default_limit_length")

    assert_failure(
        user_id.to_result(), value_is_instance_of=InputExceedLengthLimitError
    )
