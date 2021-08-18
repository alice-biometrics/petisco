import pytest

from petisco.domain.value_objects.string_value_object import (
    StringValueObject,
    InvalidStringValueObjectError,
)
from petisco.domain.value_objects.value_object import ValueObjectError


@pytest.mark.unit
def test_should_string_value_object_construct():
    value = "acme"
    vo = StringValueObject(value)

    assert vo.value == value


@pytest.mark.unit
def test_should_inherit_from_string_value_object_and_construct():
    class Name(StringValueObject):
        pass

    value = "acme"

    name = Name(value)

    assert isinstance(name, Name)
    assert name.value == value


@pytest.mark.unit
def test_should_inherit_from_string_value_object_and_add_an_ensure_clause():
    class Name(StringValueObject):
        def __init__(self, value: str):
            super(Name, self).__init__(value)

        def guard(self):
            self._ensure_name_is_less_than_30_chars()

        def _ensure_name_is_less_than_30_chars(self):
            if len(self.value) >= 30:
                raise ValueObjectError()

    value = "acme"
    name = Name(value)

    assert isinstance(name, Name)
    assert name.value == value

    invalid_value = "a" * 35
    with pytest.raises(ValueObjectError):
        Name(invalid_value)


@pytest.mark.unit
@pytest.mark.parametrize("value", ["Alex", "Íñigo", "João"])
def test_should_inherit_from_string_value_object_with_disallowed_utf8mb4_and_create_objects_successfully(
    value,
):
    class Name(StringValueObject):
        def __init__(self, value: str):
            super(Name, self).__init__(value)

        def guard(self):
            self._ensure_value_contains_valid_char(allow_utf8mb4=False)

    name = Name(value)
    assert isinstance(name, Name)
    assert name.value == value


@pytest.mark.unit
@pytest.mark.parametrize("value", ["𝘼𝙡𝙚𝙭", "Alex𖥔", "Alex😃"])
def test_should_inherit_from_string_value_object_with_disallowed_utf8mb4_and_raise_exception_with_utf8mb4_values(
    value,
):
    class Name(StringValueObject):
        def __init__(self, value: str):
            super(Name, self).__init__(value)

        def guard(self):
            self._ensure_value_contains_valid_char(allow_utf8mb4=False)

    with pytest.raises(InvalidStringValueObjectError):
        Name(value)
