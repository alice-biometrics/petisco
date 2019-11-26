import pytest

from petisco import CorrelationId
from petisco.domain.entities.client_id import ClientId
from petisco.domain.entities.user_id import UserId
from petisco.events.event import Event


class UserCreated(Event):
    user_id: UserId
    client_id: ClientId
    version: str
    correlation_id: CorrelationId = None

    def __init__(
        self,
        user_id: UserId,
        client_id: ClientId,
        correlation_id: CorrelationId,
        version: str = "1.0.0",
    ):
        self.user_id = user_id
        self.client_id = client_id
        self.correlation_id = correlation_id
        self.version = version
        super().__init__()


@pytest.mark.unit
def test_should_create_an_event_and_check_to_dict_from_dict(
    given_any_user_id, given_any_client_id, given_any_correlation_id
):

    event = UserCreated(
        user_id=given_any_user_id,
        client_id=given_any_client_id,
        correlation_id=given_any_correlation_id,
    )

    event_dict = event.to_dict()

    retrieved_event = UserCreated.from_dict(event_dict)

    assert event == retrieved_event
    assert event.user_id == given_any_user_id
    assert event.client_id == given_any_client_id


@pytest.mark.unit
def test_should_create_an_event_and_check_to_json_from_json(
    given_any_user_id, given_any_client_id, given_any_correlation_id
):

    event = UserCreated(
        user_id=given_any_user_id,
        client_id=given_any_client_id,
        correlation_id=given_any_correlation_id,
    )

    event_json = event.to_json()
    retrieved_event = UserCreated.from_json(event_json)

    assert event == retrieved_event


@pytest.mark.unit
def test_should_load_an_event_agnostically(
    given_any_user_id, given_any_client_id, given_any_correlation_id
):

    event = UserCreated(
        user_id=given_any_user_id,
        client_id=given_any_client_id,
        correlation_id=given_any_correlation_id,
    )

    event_json = event.to_json()
    agnostic_event = Event.from_json(event_json)

    assert event == agnostic_event
