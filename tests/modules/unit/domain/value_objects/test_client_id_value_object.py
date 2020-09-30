import pytest
from meiga import Success
from meiga.assertions import assert_failure
from meiga.decorators import meiga

from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.errors.given_input_is_not_valid_error import (
    GivenInputIsNotValidError,
)
from petisco.domain.errors.length_limit_string_value_object_error import (
    ExceedLengthLimitValueObjectError,
)


@pytest.mark.unit
def test_should_declare_a_valid_client_id():
    value = "Acme"
    client_id = ClientId(value)

    assert isinstance(client_id, ClientId)
    assert client_id.value == value


@pytest.mark.unit
def test_should_declare_a_client_id_with_empty_string():
    value = ""
    client_id = ClientId(value)

    assert isinstance(client_id, ClientId)
    assert client_id.value == value


@pytest.mark.unit
def test_should_declare_a_name_that_exceeds_default_length_limits():

    with pytest.raises(ExceedLengthLimitValueObjectError):
        ClientId(
            "La Corporación Acme es una empresa ficticia, que existe en el universo de los Looney Tunes. Apareció la mayor cantidad de veces en las caricaturas de El Coyote y el Correcaminos, que hicieron famosa a Acme por sus productos peligrosos y poco reales, los cuales fallaban catastróficamente de las peores maneras."
        )


@pytest.mark.unit
def test_should_declare_a_name_with_js_injection():
    with pytest.raises(GivenInputIsNotValidError):
        ClientId("<script>evil()</script>")


@pytest.mark.unit
def test_should_fail_when_declare_a_non_valid_client_id_call_guard():
    @meiga
    def controller():
        user_id = ClientId("<script>evil()</script>")
        return Success(user_id)

    result = controller()
    assert_failure(result, value_is_instance_of=GivenInputIsNotValidError)
