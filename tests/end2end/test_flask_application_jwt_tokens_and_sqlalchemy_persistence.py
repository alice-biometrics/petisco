from time import sleep

import pytest

from petisco.domain.value_objects.user_id import UserId
from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)
from petisco.persistence.sqlalchemy.sqlalchemy_extension_is_installed import (
    sqlalchemy_extension_is_installed,
)


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
@pytest.mark.skipif(
    not sqlalchemy_extension_is_installed(),
    reason="SQLAlchemy extension is not installed",
)
def test_should_return_200_when_call_a_entry_point_with_required_jwt_type_token(
    client_app, given_auth_token_headers_creator, given_any_name
):

    headers = given_auth_token_headers_creator(type_token="ADMIN_TOKEN")

    response = client_app.post(
        "/petisco/user", headers=headers, data=dict(name=given_any_name.value)
    )

    sleep(1.0)

    assert response.status_code == 200


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
@pytest.mark.skipif(
    not sqlalchemy_extension_is_installed(),
    reason="SQLAlchemy extension is not installed",
)
def test_should_return_401_when_call_a_entry_point_with_required_jwt_type_token(
    client_app, given_auth_token_headers_creator, given_any_name
):

    headers = given_auth_token_headers_creator(type_token="INVALID_TOKEN")

    response = client_app.post(
        "/petisco/user", headers=headers, data=dict(name=given_any_name)
    )
    assert response.status_code == 401
    assert response.json["error"]["type"] == "InvalidTokenHttpError"


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
@pytest.mark.skipif(
    not sqlalchemy_extension_is_installed(),
    reason="SQLAlchemy extension is not installed",
)
def test_should_return_200_when_call_a_entry_point_with_required_jwt_type_token_and_user_id(
    client_app, given_auth_token_headers_creator, given_any_name
):
    headers = given_auth_token_headers_creator(type_token="ADMIN_TOKEN")

    response = client_app.post(
        "/petisco/user", headers=headers, data=dict(name=given_any_name.value)
    )

    sleep(1.0)

    assert response.status_code == 200
    user_id = response.json["user_id"]

    headers_with_user = given_auth_token_headers_creator(
        type_token="USER_TOKEN", user_id=UserId(user_id)
    )

    response = client_app.get("/petisco/user/name", headers=headers_with_user)
    assert response.json["name"] == given_any_name.value


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
@pytest.mark.skipif(
    not sqlalchemy_extension_is_installed(),
    reason="SQLAlchemy extension is not installed",
)
def test_should_return_401_when_call_a_entry_point_with_required_jwt_type_token_with_user_and_user_is_not_available(
    client_app, given_auth_token_headers_creator
):

    headers = given_auth_token_headers_creator(type_token="USER_TOKEN")

    response = client_app.get("/petisco/user/name", headers=headers)

    assert response.status_code == 401
