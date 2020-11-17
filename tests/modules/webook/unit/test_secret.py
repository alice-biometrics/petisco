import pytest

from petisco import Secret, NotHasSpecificLengthValueObjectError


@pytest.mark.unit
def test_should_construct_a_valid_secret():
    _ = Secret("9464a12f2186cdfe38fd1cfd797758c47c544e99")


@pytest.mark.unit
def test_should_construct_a_invalid_length_secret():
    with pytest.raises(NotHasSpecificLengthValueObjectError):
        _ = Secret("00F0020007700634222")


# @pytest.mark.unit
# def test_should_raise_an_error_when_construct_a_secret_with_non_hex_values():
#     with pytest.raises(SecretIsNotHexError):
#         _ = Secret("nont-valid-secret")
