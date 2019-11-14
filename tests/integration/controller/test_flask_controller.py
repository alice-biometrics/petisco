import pytest

from petisco.frameworks.flask.flask_extension_is_installed import (
    flask_extension_is_installed,
)


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_healthcheck_with_happy_path(client):
    headers = {"Accept": "application/json"}
    response = client.open("/petisco/healthcheck", method="GET", headers=headers)
    assert 200 == response.status_code


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_environment_with_happy_path_with_apikey(
    client, given_any_apikey
):
    headers = {"Accept": "application/json", "apikey": given_any_apikey}
    response = client.open("/petisco/environment", method="GET", headers=headers)
    assert 200 == response.status_code


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_environment_with_happy_path_without_apikey(client):
    headers = {"Accept": "application/json"}
    response = client.open("/petisco/environment", method="GET", headers=headers)
    assert 401 == response.status_code


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
    assert 200 == response.status_code
    assert 5 == response.json["result"]


@pytest.mark.integration
@pytest.mark.skipif(
    not flask_extension_is_installed(), reason="Flask extension is not installed"
)
def test_should_return_200_when_call_sum_without_required_value(client):
    headers = {"Content-Type": "multipart/form-data"}
    multipart_data = dict(value_1=2)
    response = client.open(
        "/petisco/sum",
        method="POST",
        headers=headers,
        data=multipart_data,
        content_type="multipart/form-data",
    )
    assert 400 == response.status_code

