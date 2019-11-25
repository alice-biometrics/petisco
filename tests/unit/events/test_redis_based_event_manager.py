from time import sleep

import pytest
from fakeredis import FakeRedis

from petisco.events.event import Event
from petisco.events.redis.event_from_redis_message import event_from_redis_message
from petisco.events.redis.redis_based_event_manager import RedisBasedEventManager


def await_for_events():
    sleep(0.2)


@pytest.mark.unit
def test_should_create_a_redis_based_event_manager_and_publish_two_different_events():
    given_any_user_id = "user_id"
    given_any_first_name = "username"
    given_any_topic = "topic"

    class UserCreated(Event):
        user_id: str

    class FirstNameAdded(Event):
        user_id: str
        first_name: str

    global received_events
    received_events = []

    def redis_event_handler(message):
        event = event_from_redis_message(message)

        global received_events
        received_events.append(event)

        if isinstance(event, UserCreated):
            assert event.data["user_id"] == "user_id"
        elif isinstance(event, FirstNameAdded):
            assert event.data["user_id"] == "user_id"
            assert event.data["first_name"] == "username"

    event_manager = RedisBasedEventManager(
        redis=FakeRedis(), subscribers={given_any_topic: redis_event_handler}
    )

    event_manager.send(given_any_topic, UserCreated(user_id=given_any_user_id))
    event_manager.send(
        given_any_topic,
        FirstNameAdded(user_id=given_any_user_id, first_name=given_any_first_name),
    )

    await_for_events()

    event_manager.unsubscribe_all()

    assert len(received_events) == 2


@pytest.mark.unit
def test_should_unsubscribe_all_successfully():
    given_any_user_id_1 = "user_id_1"
    given_any_user_id_2 = "user_id_2"
    given_any_topic = "topic"

    class UserCreated(Event):
        user_id: str

    def redis_event_handler(message):
        event = event_from_redis_message(message)

        global received_events
        received_events.append(event)

        if isinstance(event, UserCreated):
            assert event.data["user_id"] == "user_id_1"

    event_manager = RedisBasedEventManager(
        redis=FakeRedis(), subscribers={given_any_topic: redis_event_handler}
    )

    event_manager.send(given_any_topic, UserCreated(user_id=given_any_user_id_1))
    event_manager.unsubscribe_all()
    event_manager.send(given_any_topic, UserCreated(user_id=given_any_user_id_2))

    await_for_events()

    assert len(received_events) == 2