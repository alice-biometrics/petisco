from __future__ import annotations

from redis.client import Redis
from redis.cluster import RedisCluster

from petisco.base.domain.message.command import Command
from petisco.extra.redis.application.message.bus.redis_message_bus import (
    RedisMessageBus,
)


class RedisCommandBus(RedisMessageBus):
    """
    An implementation of CommandBus using Redis infrastructure.
    """

    def __init__(self, organization: str, service: str, redis_database: Redis | RedisCluster):
        super().__init__(organization, service, redis_database, "commands")

    def dispatch(self, command: Command | list[Command]) -> None:
        """
        Dispatch one Command
        """
        commands = self._check_input(command)
        self.save(commands)
