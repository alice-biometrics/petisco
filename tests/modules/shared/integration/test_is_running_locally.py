import pytest
import requests
import requests_mock
from meiga.assertions import assert_success, assert_failure

from petisco import (
    Request,
    MissingSchemaRequestError,
    TimeoutRequestError,
    ConnectionRequestError,
    BadRequestError,
    UnauthorizedRequestError,
    UnknownRequestError,
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
def test_should_success_when_request_patch(given_any_url):
    with requests_mock.Mocker() as m:
        m.patch(given_any_url)
        result = Request.patch(given_any_url)
        assert_success(result)


@pytest.mark.integration
def test_should_success_when_request_delete(given_any_url):
    with requests_mock.Mocker() as m:
        m.delete(given_any_url)
        result = Request.delete(given_any_url)
        assert_success(result)


@pytest.mark.integration
@pytest.mark.parametrize("method", ["GET", "POST", "PATCH", "DELETE"])
def test_should_fail_when_request_method_raise_unauthorized_error(
    method, given_any_url
):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, status_code=401)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=UnauthorizedRequestError)
        assert result.value.status_code == 401


@pytest.mark.integration
@pytest.mark.parametrize("method", ["GET", "POST", "PATCH", "DELETE"])
def test_should_fail_when_request_method_returns_missing_schema_error(
    method, given_any_url
):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, exc=requests.exceptions.MissingSchema)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=MissingSchemaRequestError)
        assert result.value.status_code == 422


@pytest.mark.integration
@pytest.mark.parametrize("method", ["GET", "POST", "PATCH", "DELETE"])
def test_should_fail_when_request_method_returns_timeout_error(method, given_any_url):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, exc=requests.exceptions.ConnectTimeout)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=TimeoutRequestError)
        assert result.value.status_code == 408


@pytest.mark.integration
@pytest.mark.parametrize("method", ["GET", "POST", "PATCH", "DELETE"])
def test_should_fail_when_request_method_returns_connection_error(
    method, given_any_url
):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, exc=requests.exceptions.ConnectionError)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=ConnectionRequestError)
        assert result.value.status_code == 503


@pytest.mark.integration
@pytest.mark.parametrize("method", ["GET", "POST", "PATCH", "DELETE"])
def test_should_fail_when_request_method_returns_bad_request_error(
    method, given_any_url
):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, status_code=400)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=BadRequestError)
        assert result.value.status_code == 400


@pytest.mark.integration
@pytest.mark.parametrize(
    "method,status_code",
    [
        ("GET", 100),
        ("POST", 100),
        ("PATCH", 100),
        ("DELETE", 100),
        ("GET", 300),
        ("POST", 300),
        ("PATCH", 300),
        ("DELETE", 300),
        ("GET", 500),
        ("POST", 500),
        ("PATCH", 500),
        ("DELETE", 500),
    ],
)
def test_should_fail_when_request_method_returns_unknown_error(
    method, status_code, given_any_url
):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, status_code=status_code)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=UnknownRequestError)
        assert result.value.status_code == status_code


@pytest.mark.integration
@pytest.mark.parametrize("method", ["GET", "POST", "PATCH", "DELETE"])
def test_should_fail_when_request_method_returns_unknown_error_when_raise_an_uncontrolled_exception(
    method, given_any_url
):
    with requests_mock.Mocker() as m:
        m.register_uri(method, given_any_url, exc=InterruptedError)
        result = Request.execute(given_any_url, method)
        assert_failure(result, value_is_instance_of=UnknownRequestError)
        assert result.value.status_code == 500


@pytest.mark.integration
@pytest.mark.parametrize(
    "headers,content,json,expected_headers,expected_content",
    [
        ({}, b"", None, None, None),
        ({}, None, {}, None, {}),
        ({}, b'{"body": "petisco"}', None, None, {"body": "petisco"}),
        ({"header": "petisco"}, b"", None, {"header": "petisco"}, None),
        ({}, None, {"body": "petisco"}, None, {"body": "petisco"}),
        (
            {"header": "petisco"},
            b'{"body": "petisco"}',
            None,
            {"header": "petisco"},
            {"body": "petisco"},
        ),
        ({}, None, {"body": "petisco"}, None, {"body": "petisco"}),
    ],
)
def test_should_fail_with_expected_values_when_use_request(
    headers, content, json, expected_headers, expected_content, given_any_url
):
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            given_any_url,
            headers=headers,
            content=content,
            json=json,
            status_code=400,
        )
        result = Request.get(given_any_url)
        assert_failure(result, value_is_instance_of=BadRequestError)
        assert result.value.status_code == 400
        assert result.value.headers == expected_headers
        assert result.value.content == expected_content
