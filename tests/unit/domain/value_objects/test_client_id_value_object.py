import pytest
from meiga import Success
from meiga.assertions import assert_failure, assert_success
from meiga.decorators import meiga

from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.errors.given_input_is_not_valid_error import (
    GivenInputIsNotValidError,
)
from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)


@pytest.mark.unit
def test_should_declare_a_valid_client_id():
    client_id = ClientId("Acme")

    assert_success(
        client_id.to_result(), value_is_instance_of=str, value_is_equal_to="Acme"
    )


@pytest.mark.unit
def test_should_declare_a_client_id_with_empty_string():
    client_id = ClientId("")

    assert_success(
        client_id.to_result(), value_is_instance_of=str, value_is_equal_to=""
    )


@pytest.mark.unit
def test_should_declare_a_name_that_exceeds_default_length_limits():
    client_id = ClientId(
        "La Corporación Acme es una empresa ficticia, que existe en el universo de los Looney Tunes. Apareció la mayor cantidad de veces en las caricaturas de El Coyote y el Correcaminos, que hicieron famosa a Acme por sus productos peligrosos y poco reales, los cuales fallaban catastróficamente de las peores maneras."
    )

    assert_failure(
        client_id.to_result(), value_is_instance_of=InputExceedLengthLimitError
    )


@pytest.mark.unit
def test_should_declare_a_name_with_js_injection():
    client_id = ClientId("<script>evil()</script>")

    assert_failure(
        client_id.to_result(), value_is_instance_of=GivenInputIsNotValidError
    )


@pytest.mark.unit
def test_should_fail_when_declare_a_non_valid_client_id_call_guard():
    @meiga
    def controller():
        user_id = ClientId("<script>evil()</script>").guard()
        return Success(user_id)

    result = controller()
    assert_failure(result, value_is_instance_of=GivenInputIsNotValidError)
