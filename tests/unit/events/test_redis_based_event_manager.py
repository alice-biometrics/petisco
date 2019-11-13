import pytest
from fakeredis import FakeRedis

from petisco.events.event import Event
from petisco.events.redis.redis_based_event_handler import redis_based_event_handler
from petisco.events.redis.redis_based_event_manager import RedisBasedEventManager


@pytest.mark.unit
def test_should_create_a_redis_based_event_manager_and_publish_two_different_events():
    given_any_user_id = "user_id"
    given_any_first_name = "username"

    class UserCreated(Event):
        user_id: str

    class FirstNameAdded(Event):
        user_id: str
        first_name: str

    @redis_based_event_handler
    def user_created_handler(event: Event):
        assert event.data["user_id"] == "user_id"

    @redis_based_event_handler
    def username_added_handler(event: Event):
        assert event.data["first_name"] == "given_any_first_name"

    event_manager = RedisBasedEventManager(
        redis=FakeRedis(),
        subscribers={
            "user_created": user_created_handler,
            "first_name_added": FirstNameAdded,
        },
    )

    event_manager.send("user_created", UserCreated(user_id=given_any_user_id))
    event_manager.send(
        "first_name_added",
        FirstNameAdded(user_id=given_any_user_id, first_name=given_any_first_name),
    )

    event_manager.unsubscribe_all()


@pytest.mark.unit
def test_should_unsubscribe_all_successfully():
    given_any_user_id_1 = "user_id_1"
    given_any_user_id_2 = "user_id_2"

    class UserCreated(Event):
        user_id: str

    @redis_based_event_handler
    def user_created_handler(event: Event):
        assert event.data["user_id"] == given_any_user_id_1
        assert event.data["user_id"] == given_any_user_id_2

    event_manager = RedisBasedEventManager(
        redis=FakeRedis(), subscribers={"user_created": user_created_handler}
    )

    event_manager.send("user_created", UserCreated(user_id=given_any_user_id_1))
    event_manager.unsubscribe_all()
    event_manager.send("user_created", UserCreated(user_id=given_any_user_id_2))
