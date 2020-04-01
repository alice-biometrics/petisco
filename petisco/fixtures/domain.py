import pytest

from petisco.domain.aggregate_roots.info_id import InfoId
from petisco.domain.value_objects.client_id import ClientId
from petisco.domain.value_objects.name import Name
from petisco.domain.value_objects.user_id import UserId
from petisco.domain.value_objects.correlation_id import CorrelationId


@pytest.fixture
def given_any_client_id() -> ClientId:
    return ClientId("petisco-client")


@pytest.fixture
def given_any_user_id() -> UserId:
    return UserId("userpwlxU3yGsird")


@pytest.fixture
def given_any_correlation_id() -> CorrelationId:
    return CorrelationId("crr1d")


@pytest.fixture
def given_any_info_id(
    given_any_client_id, given_any_user_id, given_any_correlation_id
) -> InfoId:
    return InfoId(given_any_client_id, given_any_user_id, given_any_correlation_id)


@pytest.fixture
def given_info_id_only_correlation_id(given_any_correlation_id) -> InfoId:
    return InfoId(correlation_id=given_any_correlation_id)


@pytest.fixture
def given_any_name() -> Name:
    return Name("Petisco")
