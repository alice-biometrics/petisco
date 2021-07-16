import pytest

from petisco import Builder


@pytest.mark.unit
def test_builder_success():
    class MyBuilder(Builder):
        @staticmethod
        def build():
            return "MyObject"

    assert "MyObject" == MyBuilder.build()
