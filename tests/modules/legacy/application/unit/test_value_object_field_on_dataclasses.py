import pytest
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from petisco.legacy import value_object_field, Uuid


@pytest.mark.unit
def test_should_construct_a_dataclass_with_value_object_field():
    @dataclass_json
    @dataclass
    class MyDataclass:
        name: str
        id_: Uuid = value_object_field(value_object_class=Uuid, default=None)

    my_dataclass = MyDataclass("my_name")
    assert my_dataclass.to_json() == '{"name": "my_name", "id_": null}'

    my_dataclass = MyDataclass("my_name", Uuid("f34dfc97-dd54-4b67-ae92-f88d7dbd2237"))
    assert (
        my_dataclass.to_json()
        == '{"name": "my_name", "id_": "f34dfc97-dd54-4b67-ae92-f88d7dbd2237"}'
    )
