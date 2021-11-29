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


@pytest.fixture
def given_any_meta_dict():
    return {"platform_name": "python"}


@pytest.fixture
def given_json_event_data_without_attributes():
    json_data = '{"data":{"meta":{"plataform_name":"iPhone 6s","system_version":"12.4","sdk_version":"1.3.7"},"version":"1","attributes":null,"id":"83D28391-A14E-4122-996D-1A8A63A0B2EA","occurred_on":"2020-07-20 10:14:54.007000","type":"sdk.onboarding.ran"}}'
    return json_data


@pytest.fixture
def given_any_event_dict_with_meta(given_any_name, given_any_meta_dict):
    event_dict = UserCreated(given_any_name).to_dict()
    event_dict["data"]["meta"] = given_any_meta_dict
    return event_dict


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
def test_should_add_default_type_message():
    default_type_message = "domain_event"
    event = UserCreated(name="user_created")
    event_dict = event.to_dict()

    retrieved_event = UserCreated.from_dict(event_dict)

    assert event == retrieved_event
    assert retrieved_event.event_type == default_type_message
    assert event_dict["data"].get("type_message") == default_type_message


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


@pytest.mark.unit
def test_should_update_event_with_info_id_without_deleting_meta_info(
    given_any_info_id, given_any_event_dict_with_meta, given_any_meta_dict
):

    event = Event.from_dict(given_any_event_dict_with_meta)
    assert event.event_meta == given_any_meta_dict

    event.add_info_id(given_any_info_id)

    expected_event_dict = {"info_id": given_any_info_id.to_dict()}
    expected_event_dict.update(given_any_meta_dict)
    assert event.to_dict()["data"]["meta"] == expected_event_dict


@pytest.mark.unit
def test_should_load_json_when_there_is_not_attribute(
    given_json_event_data_without_attributes,
):

    event = Event.from_json(given_json_event_data_without_attributes)

    assert not event.to_dict()["data"]["attributes"]


@pytest.mark.unit
def test_should_raise_an_error_when_add_info_id_with_unexpected_type(given_any_name):

    event = UserCreated(name=given_any_name)
    with pytest.raises(TypeError):
        event.add_info_id("unexpected_type")


@pytest.mark.unit
def test_should_update_meta_on_an_event_with_info_id(given_any_info_id, given_any_name):

    event = UserCreated(name=given_any_name)
    event.add_info_id(given_any_info_id)
    event.update_meta({"device": {"platform": "ios", "model": "x", "version": "14.3"}})

    event_json = event.to_json()
    agnostic_event = Event.from_json(event_json)

    assert event == agnostic_event


@pytest.mark.unit
def test_should_raise_an_error_when_update_meta_with_unexpected_type(
    given_any_info_id, given_any_name
):

    event = UserCreated(name=given_any_name)
    event.add_info_id(given_any_info_id)

    with pytest.raises(TypeError):
        event.update_meta("unexpected_type")
