import pytest


@pytest.fixture
def given_any_token_type():
    return "TOKEN"


@pytest.fixture
def given_other_token_type():
    return "REQUIRED_TOKEN"


@pytest.fixture
def given_any_token_type_with_user():
    return "USER_TOKEN"


@pytest.fixture
def given_any_decoded_token_info(given_any_token_type, given_any_client_id):
    return {
        "user_id": None,
        "client_id": given_any_client_id,
        "token_type": given_any_token_type,
    }


@pytest.fixture
def given_any_decoded_token_info_with_user(
    given_any_token_type_with_user, given_any_client_id, given_any_user_id
):
    return {
        "user_id": given_any_user_id,
        "client_id": given_any_client_id,
        "token_type": given_any_token_type_with_user,
    }
