import os
import string
import random

import pytest

from petisco import Event, EventId
from petisco.domain.value_objects.user_id import UserId


class TrackedEventsSpy:
    def __init__(self):
        self.events = {}

    def append(self, event: Event):
        if str(event.event_id) not in self.events:
            self.events[str(event.event_id)] = {"counter": 1}
        else:
            self.events[str(event.event_id)]["counter"] += 1

    def assert_number_events(self, expected_number_events: int):
        actual_number_events = len(self.events.keys())
        assert (
            actual_number_events == expected_number_events
        ), f"Expected events is {expected_number_events}, actual {actual_number_events}"

    def get_counter_by_event_id(self, event_id: EventId):
        return self.events.get(str(event_id), {}).get("counter", 0)


@pytest.fixture
def given_any_topic():
    return "topic"


@pytest.fixture
def given_random_str() -> str:
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(5))


@pytest.fixture
def given_random_organization(given_random_str) -> str:
    return f"acme-{given_random_str}"


@pytest.fixture
def given_random_service(given_random_str) -> str:
    return f"service-{given_random_str}"


@pytest.fixture
def given_random_topic(given_random_str) -> str:
    return f"topic-{given_random_str}"


@pytest.fixture
def given_a_short_message_ttl():

    original_value = os.environ.get("PETISCO_BROKER_MESSAGE_TTL")

    os.environ["PETISCO_BROKER_MESSAGE_TTL"] = "10"

    yield

    if original_value:
        os.environ["PETISCO_BROKER_MESSAGE_TTL"] = original_value


@pytest.fixture
def make_user_created_event(given_any_user_id):
    class UserCreated(Event):
        user_id: UserId

        def __init__(self, user_id: UserId):
            self.user_id = user_id
            super().__init__()

    def _make_any_user_created_event(user_id=given_any_user_id):
        return UserCreated(user_id=user_id)

    return _make_any_user_created_event


@pytest.fixture
def make_first_name_added_event(given_any_user_id, given_any_name):
    class FirstNameAdded(Event):
        user_id: UserId
        first_name: str

        def __init__(self, user_id: UserId, first_name: str):
            self.user_id = user_id
            self.first_name = first_name
            super().__init__()

    def _make_any_first_name_added_event(
        user_id=given_any_user_id, first_name=given_any_name
    ):
        return FirstNameAdded(user_id=user_id, first_name=first_name)

    return _make_any_first_name_added_event
