import pytest

from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_a_entry_point_with_required_jwt_type_token(
    client, given_auth_token_headers_creator, given_any_name
):

    headers = given_auth_token_headers_creator(type_token="ADMIN_TOKEN")

    response = client.open(
        "/petisco/user", method="POST", headers=headers, data=dict(name=given_any_name)
    )
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_401_when_call_a_entry_point_with_required_jwt_type_token(
    client, given_auth_token_headers_creator, given_any_name
):

    headers = given_auth_token_headers_creator(type_token="INVALID_TOKEN")

    response = client.open(
        "/petisco/user", method="POST", headers=headers, data=dict(name=given_any_name)
    )
    assert response.status_code == 401
    assert response.json["error"]["type"] == "InvalidTokenHttpError"


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_a_entry_point_with_required_jwt_type_token_and_user_id(
    client,
    database,
    given_auth_token_headers_creator,
    given_any_user_id,
    given_any_name,
):
    headers = given_auth_token_headers_creator(type_token="ADMIN_TOKEN")
    response = client.open(
        "/petisco/user", method="POST", headers=headers, data=dict(name=given_any_name)
    )
    assert response.status_code == 200
    user_id = response.json["user_id"]

    headers = given_auth_token_headers_creator(type_token="USER_TOKEN", user_id=user_id)

    response = client.open("/petisco/user/name", method="GET", headers=headers)
    assert response.json["name"] == given_any_name


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_401_when_call_a_entry_point_with_required_jwt_type_token_with_user_and_user_is_not_available(
    client, given_auth_token_headers_creator
):

    headers = given_auth_token_headers_creator(type_token="USER_TOKEN")

    response = client.open("/petisco/user", method="GET", headers=headers)

    assert response.status_code == 401
