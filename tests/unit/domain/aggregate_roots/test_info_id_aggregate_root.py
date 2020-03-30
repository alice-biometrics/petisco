import pytest
from meiga.assertions import assert_success

from petisco.domain.aggregate_roots.info_id import InfoId


@pytest.mark.unit
def test_should_check_info_id_to_result_method(given_any_info_id):
    info_id = given_any_info_id

    assert_success(info_id.to_result(), value_is_instance_of=InfoId)


@pytest.mark.unit
def test_should_check_info_id_get_http_headers_method(given_any_info_id):
    info_id = given_any_info_id

    headers = info_id.get_http_headers()

    assert headers["X-Onboarding-ClientId"] == str(info_id.client_id)
    assert headers["X-Onboarding-UserId"] == str(info_id.user_id)
    assert headers["X-Correlation-Id"] == str(info_id.correlation_id)


@pytest.mark.unit
def test_should_create_from_headers(
    given_any_client_id, given_any_user_id, given_any_correlation_id
):
    headers = {
        "X-Onboarding-ClientId": str(given_any_client_id),
        "X-Onboarding-UserId": str(given_any_user_id),
        "X-Correlation-Id": str(given_any_correlation_id),
    }

    info_id = InfoId.from_headers(headers)

    assert headers["X-Onboarding-ClientId"] == str(info_id.client_id)
    assert headers["X-Onboarding-UserId"] == str(info_id.user_id)
    assert headers["X-Correlation-Id"] == str(info_id.correlation_id)


@pytest.mark.unit
def test_should_create_from_headers_empty():
    headers = {}

    info_id = InfoId.from_headers(headers)

    assert info_id.client_id is None
    assert info_id.user_id is None
    assert info_id.correlation_id is None


@pytest.mark.unit
def test_should_create_from_headers_none():

    info_id = InfoId.from_headers(None)

    assert info_id.client_id is None
    assert info_id.user_id is None
    assert info_id.correlation_id is None


@pytest.mark.unit
def test_should_create_from_headers_with_only_correlation_id(given_any_correlation_id):

    headers = {"X-Correlation-Id": str(given_any_correlation_id)}

    info_id = InfoId.from_headers(headers)

    assert info_id.client_id is None
    assert info_id.user_id is None
    assert str(info_id.correlation_id) == given_any_correlation_id
