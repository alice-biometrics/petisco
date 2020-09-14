import pytest

from petisco.domain.value_objects.correlation_id import CorrelationId
from petisco.domain.value_objects.user_id import UserId
from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)
from petisco.persistence.pymongo.mongodb_is_running_locally import (
    mongodb_is_running_locally,
)
from tests.integration.flask_app.fixtures import host, username, password, port


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
@pytest.mark.skipif(
    not mongodb_is_running_locally(
        host=host, username=username, password=password, port=port
    ),
    reason="MongoDB is not running locally",
)
def test_should_return_200_when_call_healthcheck_with_happy_path(petisco_client):
    headers = {"Accept": "toy_app/json"}
    response = petisco_client.get("/petisco/healthcheck", headers=headers)

    assert response.status_code == 200
    assert "app_name" in response.json
    assert "app_version" in response.json
    assert (
        "persistence_available" in response.json
        and response.json["persistence_available"] is True
    )


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
@pytest.mark.skipif(
    not mongodb_is_running_locally(
        host=host, username=username, password=password, port=port
    ),
    reason="MongoDB is not running locally",
)
def test_should_return_200_when_call_environment_with_happy_path_with_apikey(
    petisco_client, given_any_apikey
):
    headers = {"Accept": "toy_app/json", "apikey": given_any_apikey}
    response = petisco_client.get("/petisco/environment", headers=headers)
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
@pytest.mark.skipif(
    not mongodb_is_running_locally(
        host=host, username=username, password=password, port=port
    ),
    reason="MongoDB is not running locally",
)
def test_should_return_401_when_call_environment_with_happy_path_without_apikey(
    petisco_client
):
    headers = {"Accept": "toy_app/json"}
    response = petisco_client.get("/petisco/environment", headers=headers)
    assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
@pytest.mark.skipif(
    not mongodb_is_running_locally(
        host=host, username=username, password=password, port=port
    ),
    reason="MongoDB is not running locally",
)
def test_should_return_200_when_call_sum_with_valid_values(petisco_client):
    headers = {
        "Content-Type": "multipart/form-data",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    }

    multipart_data = dict(value_1=2, value_2=3)
    response = petisco_client.post(
        "/petisco/sum",
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
@pytest.mark.skipif(
    not mongodb_is_running_locally(
        host=host, username=username, password=password, port=port
    ),
    reason="MongoDB is not running locally",
)
def test_should_return_200_when_call_sum_with_valid_values_with_external_headers(
    petisco_client
):
    headers = {
        "Content-Type": "multipart/form-data",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "X-Correlation-Id": CorrelationId.generate().value,
        "X-Onboarding-Clientid": "petisco",
        "X-Onboarding-Userid": UserId.generate().value,
    }

    multipart_data = dict(value_1=2, value_2=3)
    response = petisco_client.post(
        "/petisco/sum",
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
@pytest.mark.skipif(
    not mongodb_is_running_locally(
        host=host, username=username, password=password, port=port
    ),
    reason="MongoDB is not running locally",
)
def test_should_return_400_when_call_sum_without_required_value(petisco_client):
    headers = {"Content-Type": "multipart/form-data"}
    multipart_data = dict(value_1=2)
    response = petisco_client.post(
        "/petisco/sum",
        headers=headers,
        data=multipart_data,
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
