import pytest

from petisco import CorrelationId
from petisco.domain.entities.client_id import ClientId
from petisco.domain.entities.user_id import UserId


@pytest.fixture
def given_any_user_id():
    return UserId("Any User")


@pytest.fixture
def given_any_client_id():
    return ClientId("Any User")


@pytest.fixture
def given_any_correlation_id():
    return CorrelationId("correlation_id")
