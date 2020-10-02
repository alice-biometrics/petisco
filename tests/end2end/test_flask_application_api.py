from time import sleep

import pytest

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
def test_should_return_200_when_create_an_user(
    petisco_client_flask_app, given_auth_token_headers_creator, given_any_name
):
    headers = given_auth_token_headers_creator(type_token="ADMIN_TOKEN")

    response = petisco_client_flask_app.post(
        "/petisco/user", headers=headers, data=dict(name=given_any_name.value)
    )
    assert response.status_code == 200

    sleep(1.0)

    response = petisco_client_flask_app.get("/petisco/users/count", headers=headers)
    assert response.status_code == 200
    assert response.json == {"users_count": 1}
