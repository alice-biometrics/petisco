import pytest

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.domain.value_objects.correlation_id import CorrelationId


@pytest.mark.unit
def test_should_check_info_id_to_dict_method(
    given_any_info_id, given_any_client_id, given_any_user_id, given_any_correlation_id
):
    info_id = given_any_info_id

    assert info_id.to_dict() == {
        "client_id": given_any_client_id.value,
        "user_id": given_any_user_id.value,
        "correlation_id": given_any_correlation_id.value,
        "ip": None,
    }


@pytest.mark.unit
def test_should_check_info_id_get_http_headers_method(given_any_info_id):
    info_id = given_any_info_id

    headers = info_id.get_http_headers()

    assert headers["X-Onboarding-Clientid"] == info_id.client_id.value
    assert headers["X-Onboarding-Userid"] == info_id.user_id.value
    assert headers["X-Correlation-Id"] == info_id.correlation_id.value


@pytest.mark.unit
def test_should_create_info_id_from_headers(
    given_any_client_id, given_any_user_id, given_any_correlation_id
):
    headers = {
        "X-Onboarding-Clientid": given_any_client_id.value,
        "X-Onboarding-Userid": given_any_user_id.value,
        "X-Correlation-Id": given_any_correlation_id.value,
    }

    info_id = InfoId.from_headers(headers)

    assert headers["X-Onboarding-Clientid"] == info_id.client_id.value
    assert headers["X-Onboarding-Userid"] == info_id.user_id.value
    assert headers["X-Correlation-Id"] == info_id.correlation_id.value


@pytest.mark.unit
def test_should_create_info_id_from_headers_empty():
    headers = {}

    info_id = InfoId.from_headers(headers)

    assert info_id.client_id is None
    assert info_id.user_id is None
    assert info_id.correlation_id is not None  # autogenerated


@pytest.mark.unit
def test_should_create_info_id_from_headers_none():

    info_id = InfoId.from_headers(None)

    assert info_id.client_id is None
    assert info_id.user_id is None
    assert info_id.correlation_id is not None  # autogenerated


@pytest.mark.unit
def test_should_create_info_id_from_headers_with_only_correlation_id(
    given_any_correlation_id
):

    headers = {"X-Correlation-Id": given_any_correlation_id.value}

    info_id = InfoId.from_headers(headers)

    assert info_id.client_id is None
    assert info_id.user_id is None
    assert info_id.correlation_id == given_any_correlation_id


@pytest.mark.unit
def test_should_update_info_id_from_headers(given_any_info_id):

    external_correlation_id = CorrelationId.generate().value

    headers = {"X-Correlation-Id": external_correlation_id}

    info_id = given_any_info_id
    autogenerated_correlation_id = info_id.correlation_id

    returned_info_id = info_id.update_from_headers(headers)

    assert info_id.correlation_id.value == external_correlation_id
    assert info_id.correlation_id != autogenerated_correlation_id
    assert returned_info_id == info_id
