from typing import Dict

import pytest

from petisco import Name
from petisco.events.event import Event


class UserCreated(Event):
    info_id: Dict[str, str]
    name: Name
    event_version: str

    def __init__(self, info_id: Dict[str, str], name: Name, version: str = "1.0.0"):
        self.info_id = info_id
        self.name = name
        self.event_version = version
        super().__init__()


@pytest.mark.unit
def test_should_create_an_event_and_check_to_dict_from_dict(
    given_any_info_id, given_any_name
):

    event = UserCreated(info_id=given_any_info_id.to_dict(), name=given_any_name)

    event_dict = event.to_dict()

    retrieved_event = UserCreated.from_dict(event_dict)

    assert event == retrieved_event
    assert event.info_id == given_any_info_id.to_dict()
    assert event.name == given_any_name


@pytest.mark.unit
def test_should_create_an_event_and_check_to_json_from_json(
    given_any_info_id, given_any_name
):

    event = UserCreated(info_id=given_any_info_id.to_dict(), name=given_any_name)

    event_json = event.to_json()
    retrieved_event = UserCreated.from_json(event_json)

    assert event == retrieved_event


@pytest.mark.unit
def test_should_load_an_event_agnostically(given_any_info_id, given_any_name):

    event = UserCreated(info_id=given_any_info_id.to_dict(), name=given_any_name)

    event_json = event.to_json()
    agnostic_event = Event.from_json(event_json)

    assert event == agnostic_event
