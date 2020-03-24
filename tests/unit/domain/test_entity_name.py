import pytest
from meiga import Success
from meiga.assertions import assert_failure, assert_success
from meiga.decorators import meiga

from petisco.domain.entities.name import Name
from petisco.domain.errors.given_name_is_not_valid_error import GivenNameIsNotValidError
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

    assert_failure(name.to_result(), value_is_instance_of=GivenNameIsNotValidError)


@pytest.mark.unit
def test_should_declare_a_name_with_none_string():
    # This is quite typical using frameworks as connexion

    name = Name("None")

    assert_success(name.to_result(), value_is_equal_to=None)


@pytest.mark.unit
def test_should_declare_a_name_with_empty_string():

    name = Name("")

    assert_success(name.to_result(), value_is_instance_of=str, value_is_equal_to="")


@pytest.mark.unit
@pytest.mark.parametrize(
    "input_name",
    [
        "毛泽东",
        "Milošević",
        "Müller",
        "Conceição",
        "Björk Guðmundsdóttir",
        "María-Jose Carreño Quiñones",
        "Борис Николаевич Ельцин",
        "John Q. Public",
        "John F.",
        "Nguyễn Tấn Dũng",
        "Øåąćłńśź",
        "öêãàõâôñ",
        "แมว",  # not working with thai marks ม้
        "Tōkairin",
    ],
)
def test_should_declare_a_valid_name_parametrizable(input_name):
    name = Name(input_name)

    assert_success(
        name.to_result(), value_is_instance_of=str, value_is_equal_to=input_name
    )


@pytest.mark.unit
def test_should_fail_when_declare_an_empty_name_and_call_guard():
    @meiga
    def controller():
        user_id = Name(
            'Rosalia de Castro: "Adios rios adios fontes; adios, regatos pequenos; adios, vista dos meus ollos: non sei cando nos veremos."'
        ).guard()
        return Success(user_id)

    result = controller()
    assert_failure(result, value_is_instance_of=InputExceedLengthLimitError)
