from __future__ import annotations

from redis.client import Redis
from redis.cluster import RedisCluster

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.extra.redis.application.message.bus.redis_message_bus import (
    RedisMessageBus,
)


class RedisDomainEventBus(RedisMessageBus):
    """
    An implementation of DomainEventBus using Redis infrastructure.
    """

    def __init__(self, organization: str, service: str, redis_database: Redis | RedisCluster):
        super().__init__(organization, service, redis_database, "events")

    def publish(self, domain_event: DomainEvent | list[DomainEvent]) -> None:
        """
        Publish a DomainEvent or a list of DomainEvent
        """
        domain_events = self._check_input(domain_event)
        self.save(domain_events)
