import pytest
from meiga import Success
from meiga.assertions import assert_failure
from meiga.decorators import meiga

from petisco.domain.value_objects.name import Name
from petisco.domain.errors.given_name_is_not_valid_error import GivenNameIsNotValidError
from petisco.domain.errors.length_limit_string_value_object_error import (
    ExceedLengthLimitValueObjectError,
)


@pytest.mark.unit
def test_should_declare_a_valid_name():

    value = "Rosalia"
    name = Name(value)

    assert isinstance(name, Name)
    assert name.value == value


@pytest.mark.unit
def test_should_declare_a_name_that_exceeds_default_length_limits():

    with pytest.raises(ExceedLengthLimitValueObjectError):
        Name(
            "Rosalia de Castro. Adios rios adios fontes, adios, regatos pequenos, adios, vista dos meus ollos, non sei cando nos veremos."
        )


@pytest.mark.unit
def test_should_declare_a_name_with_js_injection():

    with pytest.raises(GivenNameIsNotValidError):
        Name("<script>evil()</script>")


@pytest.mark.unit
def test_should_declare_a_name_with_empty_string():
    value = ""
    name = Name(value)

    assert isinstance(name, Name)
    assert name.value == value


@pytest.mark.unit
def test_should_raise_given_name_is_not_valid_when_value_is_not_a_string():

    with pytest.raises(GivenNameIsNotValidError):
        Name([0, 0])


@pytest.mark.unit
def test_should_raise_given_name_is_not_valid_when_value_is_a_string_with_4_byte_utf_chars():

    with pytest.raises(GivenNameIsNotValidError):
        Name("𝘼𝙡𝙚𝙭")


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
        "O'Connor",
    ],
)
def test_should_declare_a_valid_name_parametrizable(input_name):
    name = Name(input_name)

    assert isinstance(name.value, str)
    assert name.value == input_name


@pytest.mark.unit
def test_should_fail_when_declare_a_large_name_on_a_meiga_decorated_method():
    @meiga
    def controller():
        name = Name(
            "Rosalia de Castro. Adios rios adios fontes, adios, regatos pequenos, adios, vista dos meus ollos, non sei cando nos veremos."
        )
        return Success(name)

    result = controller()
    assert_failure(result, value_is_instance_of=ExceedLengthLimitValueObjectError)


@pytest.mark.unit
def test_should_fail_when_declare_a_no_valid_name_on_a_meiga_decorated_method():
    @meiga
    def controller():
        name = Name("<script>evil()</script>")
        return Success(name)

    result = controller()
    assert_failure(result, value_is_instance_of=GivenNameIsNotValidError)
