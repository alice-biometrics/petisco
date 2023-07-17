from pathlib import Path

import pytest
from pydantic import BaseModel

from petisco import InvalidValueObject, ValueObject


@pytest.mark.unit
class TestValueObject:
    @pytest.mark.parametrize(
        "expected_value", ["any", 1, 0.3, ["1", ["2"]], {"any": 1}]
    )
    def should_construct_and_serialize_with_inner_value(self, expected_value):  # noqa
        value_object = ValueObject(value=expected_value)
        assert value_object.value == expected_value
        assert value_object.model_dump() == expected_value

    @pytest.mark.parametrize(
        "expected_value", ["any", 1, 0.3, ["1", ["2"]], {"any": 1}]
    )
    def should_fail_when_try_to_change_a_parameter(self, expected_value):  # noqa
        value_object = ValueObject(value=expected_value)

        with pytest.raises(TypeError) as excinfo:
            value_object.value = expected_value

        assert "ValueObject objects are immutable" in str(excinfo.value)

    @pytest.mark.parametrize(
        "expected_value", ["any", 1, 0.3, ["1", ["2"]], {"any": 1}]
    )
    def should_equal_when_values_are_equals(self, expected_value):  # noqa
        value_object = ValueObject(value=expected_value)
        other = ValueObject(value=expected_value)

        assert value_object == other
        assert id(value_object) != id(other)

    def should_raise_invalid_value_object_error_when_value_is_none(self):  # noqa
        with pytest.raises(InvalidValueObject) as excinfo:
            ValueObject(value=None)
        assert "InvalidValueObject" in str(excinfo.value)

    def should_check_is_hashable(self):  # noqa
        value_object = ValueObject(value=1)
        hash_value_object = hash(value_object)
        assert hash_value_object == 1

    def should_check_encode_decode(self):  # noqa
        value_object = ValueObject(value=1)

        filename = ".tmp.json"
        path = Path(filename)
        path.write_text(value_object.model_dump_json())
        value_object_parsed = ValueObject.parse_file(filename)
        assert value_object == value_object_parsed
        path.unlink()

    def should_check_value_object_serializer(self):  # noqa
        expected_value = "my_expected_value"

        class MyValueObject(ValueObject):
            ...

        class MyModel(BaseModel):
            my_value_object: MyValueObject

            _my_value_object = ValueObject.serializer("my_value_object")

        my_model = MyModel(my_value_object=MyValueObject(expected_value))

        assert my_model.model_dump() == {"my_value_object": expected_value}
