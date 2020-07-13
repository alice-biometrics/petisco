import pytest
import requests
import requests_mock
from meiga.assertions import assert_success, assert_failure

from petisco import (
    Request,
    MissingSchemaRequestError,
    TimeoutRequestError,
    ConnectionRequestError,
)


@pytest.fixture
def given_any_url():
    return "http://alicebiometrics.com"


@pytest.fixture
def given_invalid_url():
    return "invalid_url"


@pytest.mark.integration
def test_should_success_when_request_get(given_any_url):
    with requests_mock.Mocker() as m:
        m.get(given_any_url)
        result = Request.get(given_any_url)
        assert_success(result)


@pytest.mark.integration
def test_should_success_when_request_post(given_any_url):
    with requests_mock.Mocker() as m:
        m.post(given_any_url)
        result = Request.post(given_any_url)
        assert_success(result)


@pytest.mark.integration
def test_should_success_when_request_delete(given_any_url):
    with requests_mock.Mocker() as m:
        m.delete(given_any_url)
        result = Request.delete(given_any_url)
        assert_success(result)


@pytest.mark.integration
@pytest.mark.parametrize("method", ["GET", "POST", "DELETE"])
def test_should_fail_when_request_method_raise_missing_schema_error(
    method, given_any_url
):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, exc=requests.exceptions.MissingSchema)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=MissingSchemaRequestError)


@pytest.mark.integration
@pytest.mark.parametrize("method", ["GET", "POST", "DELETE"])
def test_should_fail_when_request_method_raise_timeout_error(method, given_any_url):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, exc=requests.exceptions.ConnectTimeout)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=TimeoutRequestError)


@pytest.mark.integration
@pytest.mark.parametrize("method", ["GET", "POST", "DELETE"])
def test_should_fail_when_request_method_raise_connection_error(method, given_any_url):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, exc=requests.exceptions.ConnectionError)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=ConnectionRequestError)