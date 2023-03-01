import json

import pytest
from fakeredis import FakeRedis

from petisco import DomainEvent
from petisco.extra.redis import RedisCommandBus
from tests.modules.extra.rabbitmq.mother.domain_event_user_created_mother import (
    DomainEventUserCreatedMother,
)
from tests.modules.extra.redis.mother.redis_domain_event_bus_mother import (
    RedisDomainEventBusMother,
)


@pytest.mark.integration
class TestRedisDomainEventBus:
    domain_event: DomainEvent
    redis_database: FakeRedis

    def setup_method(self):
        self.domain_event = DomainEventUserCreatedMother.random()
        self.redis_database = FakeRedis()

    def teardown_method(self):
        self.redis_database.flushall()

    def _assert_domain_event_is_saved_in_bus(
        self, bus: RedisCommandBus, domain_event: DomainEvent
    ):
        data = self.redis_database.lrange(bus.database_name, 0, -1)
        domain_events = [
            DomainEvent.from_dict(json.loads(command_data).get("message"))
            for command_data in data
        ]
        assert domain_events[0] == domain_event

    def _assert_numer_of_domain_events(self, bus: RedisCommandBus, number: int):
        domain_events = self.redis_database.lrange(bus.database_name, 0, -1)
        assert len(domain_events) == 3

    def should_publish_domain_event(self):
        bus = RedisDomainEventBusMother.default(self.redis_database)
        bus.publish(self.domain_event)

        self._assert_domain_event_is_saved_in_bus(bus, self.domain_event)

    def should_publish_several_domain_events(self):
        bus = RedisDomainEventBusMother.default(self.redis_database)
        bus.publish(self.domain_event)
        bus.publish(self.domain_event)
        bus.publish(self.domain_event)

        self._assert_numer_of_domain_events(bus, 3)

    def should_publish_list_several_domain_events(self):
        bus = RedisDomainEventBusMother.default(self.redis_database)
        bus.publish_list([self.domain_event, self.domain_event, self.domain_event])

        self._assert_numer_of_domain_events(bus, 3)

    def should_publish_domain_event_with_info_id(self):
        bus = RedisDomainEventBusMother.with_info_id(self.redis_database)
        bus.publish(self.domain_event)

        self._assert_domain_event_is_saved_in_bus(bus, self.domain_event)

    def should_publish_list_several_domain_events_with_info_id(self):
        bus = RedisDomainEventBusMother.with_info_id(self.redis_database)
        bus.publish_list([self.domain_event, self.domain_event, self.domain_event])

        self._assert_numer_of_domain_events(bus, 3)
