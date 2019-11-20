import pytest
from meiga.assertions import assert_failure

from petisco.domain.entities.client_id import ClientId
from petisco.domain.errors.given_input_is_not_valid_error import (
    GivenInputIsNotValidError,
)
from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)


@pytest.mark.unit
def test_should_declare_a_valid_client_id():

    name = ClientId("Acme")

    assert isinstance(name.handle(), str)
    assert name.handle() == "Acme"


@pytest.mark.unit
def test_should_declare_a_name_that_exceeds_default_length_limits():

    name = ClientId(
        "La Corporación Acme es una empresa ficticia, que existe en el universo de los Looney Tunes. Apareció la mayor cantidad de veces en las caricaturas de El Coyote y el Correcaminos, que hicieron famosa a Acme por sus productos peligrosos y poco reales, los cuales fallaban catastróficamente de las peores maneras."
    )

    assert_failure(name.handle(), value_is_instance_of=InputExceedLengthLimitError)


@pytest.mark.unit
def test_should_declare_a_name_with_js_injection():

    name = ClientId("<script>evil()</script>")

    assert_failure(name.handle(), value_is_instance_of=GivenInputIsNotValidError)
