from redis.client import Redis

from petisco.extra.redis import RedisCommandBus
from tests.modules.base.mothers.message_meta_mother import MessageMetaMother
from tests.modules.extra.rabbitmq.mother.defaults import (
    DEFAULT_ORGANIZATION,
    DEFAULT_SERVICE,
)


class RedisCommandBusMother:
    @staticmethod
    def default(redis_database: Redis):
        return RedisCommandBus(DEFAULT_ORGANIZATION, DEFAULT_SERVICE, redis_database=redis_database)

    @staticmethod
    def with_service(service: str, redis_database: Redis):
        return RedisCommandBus(DEFAULT_ORGANIZATION, service, redis_database=redis_database)

    @staticmethod
    def with_info_id(redis_database: Redis):
        return RedisCommandBus(
            DEFAULT_ORGANIZATION, DEFAULT_SERVICE, redis_database=redis_database
        ).with_meta(MessageMetaMother.with_meta_with_info())
