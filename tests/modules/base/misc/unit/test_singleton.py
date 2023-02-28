from typing import Any

import pytest

from petisco import Singleton


class MySingleton(metaclass=Singleton):
    value: str

    def __init__(self, **kwargs: Any) -> None:
        self.value = str(kwargs.get("value"))


@pytest.mark.unit
class TestSingleton:
    expected_value: str

    def setup_method(self):
        self.expected_value = "my_value"

    def teardown_method(self):
        MySingleton.clear()

    def should_create_only_one_instance(self):
        MySingleton(value=self.expected_value)
        assert MySingleton().value == self.expected_value

    def should_create_and_force_recreation(self):
        MySingleton(value="initial_value")
        assert MySingleton().value != self.expected_value
        MySingleton(value=self.expected_value, force_recreation=True)
        assert MySingleton().value == self.expected_value
