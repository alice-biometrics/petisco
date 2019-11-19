import pytest

from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_healthcheck_with_happy_path(client):
    headers = {"Accept": "toy_app/json"}
    response = client.open("/petisco/healthcheck", method="GET", headers=headers)
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_environment_with_happy_path_with_apikey(
    client, given_any_apikey
):
    headers = {"Accept": "toy_app/json", "apikey": given_any_apikey}
    response = client.open("/petisco/environment", method="GET", headers=headers)
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_401_when_call_environment_with_happy_path_without_apikey(client):
    headers = {"Accept": "toy_app/json"}
    response = client.open("/petisco/environment", method="GET", headers=headers)
    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_sum_with_valid_values(client):
    headers = {"Content-Type": "multipart/form-data"}
    multipart_data = dict(value_1=2, value_2=3)
    response = client.open(
        "/petisco/sum",
        method="POST",
        headers=headers,
        data=multipart_data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert response.json["result"] == 5


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_400_when_call_sum_without_required_value(client):
    headers = {"Content-Type": "multipart/form-data"}
    multipart_data = dict(value_1=2)
    response = client.open(
        "/petisco/sum",
        method="POST",
        headers=headers,
        data=multipart_data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_a_entry_point_with_required_jwt_type_token(
    client, given_auth_token_headers_creator
):

    headers = given_auth_token_headers_creator(type_token="ADMIN_TOKEN")

    response = client.open("/petisco/user", method="POST", headers=headers)
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_401_when_call_a_entry_point_with_required_jwt_type_token(
    client, given_auth_token_headers_creator
):

    headers = given_auth_token_headers_creator(type_token="INVALID_TOKEN")

    response = client.open("/petisco/user", method="POST", headers=headers)
    assert response.status_code == 401
    assert response.json["error"]["type"] == "InvalidTokenHttpError"


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_a_entry_point_with_required_jwt_type_token_and_user_id(
    client, given_auth_token_headers_creator
):

    headers = given_auth_token_headers_creator(
        type_token="USER_TOKEN", user_id="any_user_id"
    )

    response = client.open("/petisco/user", method="GET", headers=headers)

    assert response.status_code == 200
    assert response.json["user_id"] == "any_user_id"
