from typing import List

from redis.client import Redis

from petisco.base.domain.message.domain_event import DomainEvent
from petisco.extra.redis.application.message.bus.redis_message_bus import (
    RedisMessageBus,
)


class RedisDomainEventBus(RedisMessageBus):
    """
    An implementation of DomainEventBus using Redis infrastructure.
    """

    def __init__(self, organization: str, service: str, redis_database: Redis):
        super().__init__(organization, service, redis_database, "events")

    def publish(self, domain_event: DomainEvent) -> None:
        """
        Publish a DomainEvent
        """
        self.save(domain_event)

    def publish_list(self, domain_events: List[DomainEvent]) -> None:
        """
        Publish a list of DomainEvent
        """
        self.save_list(domain_events)
