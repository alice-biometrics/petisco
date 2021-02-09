import pytest

from petisco import StringValueObject, Uuid


@pytest.mark.unit
def test_value_object_should_check_eq_operator_comparison():
    class Name(StringValueObject):
        pass

    value = "Castelao"
    name = Name(value)
    expected_name = Name(value)

    assert name == value
    assert name == expected_name


@pytest.mark.unit
def test_value_object_should_check_ne_operator_comparison():
    class Name(StringValueObject):
        pass

    value = "Castelao"
    name = Name(value)
    other_name = Name("Rosalia")

    assert name != "Rosalia"
    assert name != other_name


@pytest.mark.unit
def test_value_object_uuid_should_check_eq_operator_comparison():

    value = "a8884fa9-3477-4533-9cd5-d99096435b31"
    id_ = Uuid(value)
    expected_id = Uuid(value)

    assert id_ == value
    assert id_ == expected_id
