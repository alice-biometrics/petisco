import pytest

from petisco import Name
from petisco.events.event import Event


class UserCreated(Event):
    name: Name

    def __init__(self, name: Name):
        self.name = name
        super().__init__()


class VersionedUserCreated(Event):
    name: Name

    def __init__(self, name: Name):
        self.name = name
        super().__init__({"event_version": 2})


@pytest.mark.unit
def test_should_create_an_event_and_check_to_dict_from_dict(
    given_any_info_id, given_any_name
):

    event = UserCreated(name=given_any_name)
    event.add_info_id(given_any_info_id)
    event_dict = event.to_dict()

    retrieved_event = UserCreated.from_dict(event_dict)

    assert event == retrieved_event
    assert event.event_info_id == given_any_info_id.to_dict()
    assert event.name == given_any_name


@pytest.mark.unit
def test_should_create_an_event_and_check_to_dict_from_dict_with_non_default_version_event(
    given_any_info_id, given_any_name
):

    event = VersionedUserCreated(name=given_any_name)
    event.add_info_id(given_any_info_id)
    event_dict = event.to_dict()

    retrieved_event = UserCreated.from_dict(event_dict)

    assert event == retrieved_event
    assert event.event_info_id == given_any_info_id.to_dict()
    assert event.name == given_any_name


@pytest.mark.unit
def test_should_create_an_event_and_check_to_json_from_json(
    given_any_info_id, given_any_name
):

    event = UserCreated(name=given_any_name)
    event.add_info_id(given_any_info_id)

    event_json = event.to_json()
    retrieved_event = UserCreated.from_json(event_json)

    assert event == retrieved_event


@pytest.mark.unit
def test_should_create_an_event_and_check_to_json_from_json_with_non_default_version_event(
    given_any_info_id, given_any_name
):

    event = VersionedUserCreated(name=given_any_name)
    event.add_info_id(given_any_info_id)

    event_json = event.to_json()
    retrieved_event = UserCreated.from_json(event_json)

    assert event == retrieved_event


@pytest.mark.unit
def test_should_load_an_event_agnostically(given_any_info_id, given_any_name):

    event = UserCreated(name=given_any_name)
    event.add_info_id(given_any_info_id)

    event_json = event.to_json()
    agnostic_event = Event.from_json(event_json)

    assert event == agnostic_event


@pytest.mark.unit
def test_should_load_an_event_agnostically_with_non_default_version_event(
    given_any_info_id, given_any_name
):

    event = VersionedUserCreated(name=given_any_name)
    event.add_info_id(given_any_info_id)

    event_json = event.to_json()
    agnostic_event = Event.from_json(event_json)

    assert event == agnostic_event
