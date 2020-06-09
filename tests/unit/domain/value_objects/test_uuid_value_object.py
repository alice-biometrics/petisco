import pytest
from petisco.domain.value_objects.uuid import Uuid, InvalidUuidError


@pytest.mark.unit
def test_should_construct_generate():
    uuid = Uuid.generate()

    assert len(uuid.value) == 36


@pytest.mark.unit
def test_should_inherit_from_uuid_and_construct_from_generated_value():
    class MyId(Uuid):
        pass

    uuid_value = Uuid.generate().value

    my_id = MyId(uuid_value)

    assert isinstance(my_id, MyId)
    assert my_id.value == uuid_value


@pytest.mark.unit
def test_should_inherit_from_uuid_and_generate():
    class MyId(Uuid):
        pass

    my_id = MyId.generate()

    assert isinstance(my_id, MyId)
    assert len(my_id.value) == 36


@pytest.mark.unit
def test_should_inherit_from_uuid_and_construct_from_invalid_value():
    class MyId(Uuid):
        pass

    invalid_value = "acme"

    with pytest.raises(InvalidUuidError) as excinfo:
        MyId(invalid_value)

    assert "acme" in str(excinfo.value)
