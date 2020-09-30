import pytest

from petisco import EventId
from tests.modules.event.unit.test_event import UserCreated


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
            "id": "e4e1d".rjust(EventId.length(), "0"),  # Refilled with zeros
            "type": "user.created",
            "version": "0",  # old format event will be set to 0 version
            "occurred_on": "2020-04-30 09:05:58.965449",
            "attributes": {"name": "Name"},
            "meta": {},
        }
    }

    retrieved_event = UserCreated.from_deprecated_dict(deprecated_body)

    assert retrieved_event.to_dict() == expected_body


@pytest.mark.unit
@pytest.mark.parametrize(
    "input_info_id,expected_info_id",
    [
        (
            {
                "client_id": "client",
                "user_id": "mwy-yQWxt2O0ECnw",
                "correlation_id": "889bd",
            },
            {
                "client_id": "client",
                "user_id": "mwy-yQWxt2O0ECnw",
                "correlation_id": "889bd",
                "ip": None,
            },
        ),
        (
            {"user_id": "mwy-yQWxt2O0ECnw", "correlation_id": "889bd"},
            {
                "client_id": None,
                "user_id": "mwy-yQWxt2O0ECnw",
                "correlation_id": "889bd",
                "ip": None,
            },
        ),
        (
            {
                "client_id": "client",
                "user_id": "mwy-yQWxt2O0ECnw",
                "correlation_id": "889bd",
                "ip": "0.0.0.0",
            },
            {
                "client_id": "client",
                "user_id": "mwy-yQWxt2O0ECnw",
                "correlation_id": "889bd",
                "ip": "0.0.0.0",
            },
        ),
    ],
)
def test_should_create_an_event_from_deprecated_version_with_info_id(
    input_info_id, expected_info_id
):

    deprecated_body = {
        "document_id": "SIgradfXfWNbtDfsA0sqwgJWpMs=",
        "manual": False,
        "event_version": "2.0.0",
        "event_id": "57062",
        "event_name": "DocumentBackRequested",
        "event_occurred_on": "2020-05-08 12:17:15.162161",
        "info_id": input_info_id,
    }
    expected_body = {
        "data": {
            "id": "57062".rjust(EventId.length(), "0"),  # Refilled with zeros
            "type": "document.back.requested",
            "version": "0",
            "occurred_on": "2020-05-08 12:17:15.162161",
            "attributes": {
                "document_id": "SIgradfXfWNbtDfsA0sqwgJWpMs=",
                "manual": False,
            },
            "meta": {"info_id": expected_info_id},
        }
    }

    retrieved_event = UserCreated.from_deprecated_dict(deprecated_body)

    assert retrieved_event.to_dict() == expected_body
