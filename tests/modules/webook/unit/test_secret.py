import pytest

from petisco import Secret, SecretIsNotHexError


@pytest.mark.unit
def test_should_construct_a_valid_secret():
    _ = Secret("00480065006C006C006F0020007700634222")


@pytest.mark.unit
def test_should_raise_an_error_when_construct_a_secret_with_non_hex_values():
    with pytest.raises(SecretIsNotHexError):
        _ = Secret("nont-valid-secret")
