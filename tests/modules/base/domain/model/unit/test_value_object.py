import pytest

from petisco import ValueObject, InvalidValueObject


@pytest.mark.unit
@pytest.mark.parametrize("expected_value", ["any", 1, 0.3, ["1", ["2"]], {"any": 1}])
def test_value_object_should_construct_and_serialize_with_inner_value(expected_value):

    value_object = ValueObject(value=expected_value)
    assert value_object.value == expected_value
    assert value_object.dict() == expected_value


@pytest.mark.unit
@pytest.mark.parametrize("expected_value", ["any", 1, 0.3, ["1", ["2"]], {"any": 1}])
def test_value_object_should_fail_when_try_to_change_a_parameter(expected_value):
    value_object = ValueObject(value=expected_value)

    with pytest.raises(TypeError) as excinfo:
        value_object.value = expected_value

    assert "ValueObject objects are immutable" in str(excinfo.value)


@pytest.mark.unit
@pytest.mark.parametrize("expected_value", ["any", 1, 0.3, ["1", ["2"]], {"any": 1}])
def test_value_object_should_equal_when_values_are_equals(expected_value):

    value_object = ValueObject(value=expected_value)
    other = ValueObject(value=expected_value)

    assert value_object == other
    assert id(value_object) != id(other)


@pytest.mark.unit
def test_value_object_with_value_none_should_raise_invalid_value_object_error():
    with pytest.raises(InvalidValueObject) as excinfo:
        ValueObject(value=None)
    assert "Invalid ValueObject" in str(excinfo.value)
