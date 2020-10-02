import pytest

from petisco import Event, EventId, NotifierMessage, InfoId
from petisco.domain.value_objects.user_id import UserId
from petisco.notifier.domain.notifier_exception_message import NotifierExceptionMessage


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
        ), f"Expected events is {expected_number_events}, actual {actual_number_events}. [{self.events}]"

    def get_counter_by_event_id(self, event_id: EventId):
        return self.events.get(str(event_id), {}).get("counter", 0)


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


@pytest.fixture
def given_any_message():
    return "Hello world"


@pytest.fixture
def given_any_title():
    return "This is a title"


@pytest.fixture
def given_any_info_petisco():
    return {
        "app_name": "test",
        "app_version": "0.0.1",
        "petisco_version": "0.0.1",
        "environment": "Production",
    }


@pytest.fixture
def given_any_basic_notifier_message(given_any_message):
    return NotifierMessage(message=given_any_message)


@pytest.fixture
def given_any_notifier_message_with_info_id(
    given_any_client_id, given_any_user_id, given_any_message
):
    return NotifierMessage(
        message=given_any_message,
        info_id=InfoId(client_id=given_any_client_id, user_id=given_any_user_id),
    )


@pytest.fixture
def given_any_complete_notifier_message(
    given_any_client_id,
    given_any_user_id,
    given_any_message,
    given_any_info_petisco,
    given_any_title,
):
    return NotifierMessage(
        title=given_any_title,
        message=given_any_message,
        info_id=InfoId(client_id=given_any_client_id, user_id=given_any_user_id),
        info_petisco=given_any_info_petisco,
    )


@pytest.fixture
def given_any_exception():
    return ValueError("Oops, something went wrong")


@pytest.fixture
def given_any_traceback():
    return """Traceback (most recent call last):
  File "e.py", line 7, in <module>
    raise TypeError("Again !?!")
TypeError: Again !?!
"""


@pytest.fixture
def given_long_traceback():
    return (
        """Traceback (most recent call last):
  File "e.py", line 7, in <module>
    raise TypeError("Again !?!")
TypeError: Again !?!
"""
        * 500
    )


@pytest.fixture
def given_any_input_parameters():
    return {"parameter_1": 1, "parameter_2": 2}


@pytest.fixture
def given_any_complete_notifier_exception_message(
    given_any_client_id,
    given_any_user_id,
    given_any_message,
    given_any_info_petisco,
    given_any_exception,
    given_any_input_parameters,
    given_any_traceback,
):
    return NotifierExceptionMessage(
        executor="test_function",
        exception=given_any_exception,
        input_parameters=given_any_input_parameters,
        traceback=given_any_traceback,
        info_id=InfoId(client_id=given_any_client_id, user_id=given_any_user_id),
        info_petisco=given_any_info_petisco,
    )


@pytest.fixture
def given_long_traceback_complete_notifier_exception_message(
    given_any_client_id,
    given_any_user_id,
    given_any_message,
    given_any_info_petisco,
    given_any_exception,
    given_long_traceback,
):
    return NotifierExceptionMessage(
        executor="test_function",
        exception=given_any_exception,
        traceback=given_long_traceback,
        info_id=InfoId(client_id=given_any_client_id, user_id=given_any_user_id),
        info_petisco=given_any_info_petisco,
    )
