import pytest

from petisco.domain.value_objects.correlation_id import CorrelationId
from petisco.domain.value_objects.user_id import UserId
from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_healthcheck_with_happy_path(client_app):
    headers = {"Accept": "application/json"}
    response = client_app.get("/petisco/healthcheck", headers=headers)

    assert response.status_code == 200
    assert "app_name" in response.json
    assert "app_version" in response.json
    assert (
        "persistence_available" in response.json
        and response.json["persistence_available"] is True
    )


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_environment_with_happy_path_with_apikey(
    client_app, given_any_apikey
):
    headers = {"Accept": "application/json", "apikey": given_any_apikey}
    response = client_app.get("/petisco/environment", headers=headers)
    assert response.status_code == 200


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_401_when_call_environment_with_happy_path_without_apikey(
    client_app
):
    headers = {"Accept": "application/json"}
    response = client_app.get("/petisco/environment", headers=headers)
    assert response.status_code == 401


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_sum_with_valid_values(client_app):
    headers = {
        "Content-Type": "multipart/form-data",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    }

    multipart_data = dict(value_1=2, value_2=3)
    response = client_app.post(
        "/petisco/sum",
        headers=headers,
        data=multipart_data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert response.json["result"] == 5


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_sum_with_valid_values_with_external_headers(
    client_app
):
    headers = {
        "Content-Type": "multipart/form-data",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "X-Correlation-Id": CorrelationId.generate().value,
        "X-Onboarding-Clientid": "petisco",
        "X-Onboarding-Userid": UserId.generate().value,
    }

    multipart_data = dict(value_1=2, value_2=3)
    response = client_app.post(
        "/petisco/sum",
        headers=headers,
        data=multipart_data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert response.json["result"] == 5


@pytest.mark.end2end
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_400_when_call_sum_without_required_value(client_app):
    headers = {"Content-Type": "multipart/form-data"}
    multipart_data = dict(value_1=2)
    response = client_app.post(
        "/petisco/sum",
        headers=headers,
        data=multipart_data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
