import pytest

from petisco import Event, Name, unique_events


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
def test_should_create_an_event_and_check_its_hash(given_any_info_id, given_any_name):

    event = UserCreated(name=given_any_name)

    hash_before_add_info_id = hash(event)

    event.add_info_id(given_any_info_id)

    hash_after_add_info_id = hash(event)

    assert hash_before_add_info_id != hash_after_add_info_id


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


@pytest.mark.unit
def test_should_check_unique_events():

    user_one = UserCreated(name=Name("one"))
    user_two = UserCreated(name=Name("two"))

    events = unique_events([user_one, user_one, user_one])
    assert len(events) == 1

    events = unique_events([user_one, user_one, user_two, user_two])
    assert len(events) == 2
