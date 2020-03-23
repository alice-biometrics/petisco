from time import sleep

import pytest
from fakeredis import FakeRedis
from petisco import RedisEventManager, event_from_redis_message, UserId


def await_for_events():
    sleep(0.2)


@pytest.mark.integration
def test_should_create_a_redis_event_manager_and_publish_two_different_events(
    make_user_created_event, make_first_name_added_event, given_any_topic
):
    given_any_user_id = "user_id"
    given_any_first_name = "username"
    given_any_topic = "topic"

    global received_events
    received_events = []

    def redis_event_handler(message):
        event = event_from_redis_message(message)

        global received_events
        received_events.append(event)

        if isinstance(event, make_user_created_event().__class__):
            assert event.user_id == "user_id"
        elif isinstance(event, make_first_name_added_event().__class__):
            assert event.user_id == "user_id"
            assert event.first_name == "Any User"

    event_manager = RedisEventManager(
        redis=FakeRedis(), subscribers={given_any_topic: redis_event_handler}
    )

    event_manager.send(
        given_any_topic, make_user_created_event(user_id=given_any_user_id)
    )
    event_manager.send(
        given_any_topic,
        make_first_name_added_event(
            user_id=given_any_user_id, first_name=given_any_first_name
        ),
    )

    await_for_events()

    event_manager.unsubscribe_all()

    assert len(received_events) == 2


@pytest.mark.integration
def test_should_unsubscribe_all_successfully(make_user_created_event):
    given_any_user_id_1 = UserId("user_id_1")
    given_any_user_id_2 = UserId("user_id_2")
    given_any_topic = "topic"

    def redis_event_handler(message):
        event = event_from_redis_message(message)

        global received_events
        received_events.append(event)

        if isinstance(event, make_user_created_event().__class__):
            assert event.user_id == "user_id_1"

    event_manager = RedisEventManager(
        redis=FakeRedis(), subscribers={given_any_topic: redis_event_handler}
    )

    event_manager.send(
        given_any_topic, make_user_created_event(user_id=given_any_user_id_1)
    )
    event_manager.unsubscribe_all()
    event_manager.send(
        given_any_topic, make_user_created_event(user_id=given_any_user_id_2)
    )

    await_for_events()

    assert len(received_events) >= 1


@pytest.mark.integration
def test_should_create_a_redis_event_manager_without_subscribers_and_publish_a_event(
    make_user_created_event, given_any_topic
):
    given_any_user_id = "user_id"

    event_manager = RedisEventManager(redis=FakeRedis())

    event_manager.send(
        given_any_topic, make_user_created_event(user_id=given_any_user_id)
    )

    event_manager.unsubscribe_all()
