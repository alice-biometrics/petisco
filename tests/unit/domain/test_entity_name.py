import pytest
from meiga.assertions import assert_failure, assert_success

from petisco.domain.entities.name import Name
from petisco.domain.errors.given_input_is_not_valid_error import (
    GivenInputIsNotValidError,
)
from petisco.domain.errors.input_exceed_lenght_limit_error import (
    InputExceedLengthLimitError,
)


@pytest.mark.unit
def test_should_declare_a_valid_name():

    name = Name("Rosalia")

    assert_success(
        name.to_result(), value_is_instance_of=str, value_is_equal_to="Rosalia"
    )


@pytest.mark.unit
def test_should_declare_a_name_that_exceeds_default_length_limits():

    name = Name(
        'Rosalia de Castro: "Adios rios adios fontes; adios, regatos pequenos; adios, vista dos meus ollos: non sei cando nos veremos."'
    )

    assert_failure(name.to_result(), value_is_instance_of=InputExceedLengthLimitError)


@pytest.mark.unit
def test_should_declare_a_name_with_js_injection():

    name = Name("<script>evil()</script>")

    assert_failure(name.to_result(), value_is_instance_of=GivenInputIsNotValidError)


@pytest.mark.unit
def test_should_declare_a_name_with_none_string():
    # This is quite typical using frameworks as connexion

    name = Name("None")

    assert_success(name.to_result(), value_is_equal_to=None)
