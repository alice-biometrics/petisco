import pytest


@pytest.mark.unit
def test_should_import_public_api():
    from petisco import public_api  # noqa
