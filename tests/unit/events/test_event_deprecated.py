import pytest

from tests.unit.events.test_event import UserCreated


@pytest.mark.unit
def test_should_create_an_event_from_deprecated_version():

    deprecated_body = {
        "name": "Name",
        "event_version": "2.0.0",
        "event_id": "e4e1d",
        "event_name": "UserCreated",
        "event_occurred_on": "2020-04-30 09:05:58.965449",
    }
    expected_body = {
        "data": {
            "id": "e4e1d",
            "type": "user.created",
            "version": "0",  # old format event will be set to 0 version
            "occurred_on": "2020-04-30 09:05:58.965449",
            "attributes": {"name": "Name"},
            "meta": {},
        }
    }

    retrieved_event = UserCreated.from_deprecated_dict(deprecated_body)

    assert retrieved_event.to_dict() == expected_body
