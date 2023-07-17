import json

import pytest
from fakeredis import FakeRedis

from petisco import Command
from petisco.extra.redis import RedisCommandBus
from tests.modules.extra.rabbitmq.mother.command_persist_user_mother import (
    CommandPersistUserMother,
)
from tests.modules.extra.redis.mother.redis_command_bus_mother import (
    RedisCommandBusMother,
)


@pytest.mark.integration
class TestRedisCommandBus:
    command: Command
    redis_database: FakeRedis

    def setup_method(self):
        self.command = CommandPersistUserMother.random()
        self.redis_database = FakeRedis()

    def teardown_method(self):
        self.redis_database.flushall()

    def _assert_command_is_saved_in_bus(self, bus: RedisCommandBus, command: Command):
        data = self.redis_database.lrange(bus.database_name, 0, -1)
        commands = [
            Command.from_format(json.loads(command_data).get("message"))
            for command_data in data
        ]
        assert commands[0] == command

    def _assert_numer_of_commands(self, bus: RedisCommandBus, number: int):
        commands = self.redis_database.lrange(bus.database_name, 0, -1)
        assert len(commands) == number

    def should_dispatch_command(self):
        bus = RedisCommandBusMother.default(self.redis_database)
        bus.dispatch(self.command)

        self._assert_command_is_saved_in_bus(bus, self.command)

    def should_dispatch_several_commands(self):
        bus = RedisCommandBusMother.default(self.redis_database)
        bus.dispatch(self.command)
        bus.dispatch(self.command)
        bus.dispatch(self.command)

        self._assert_numer_of_commands(bus, 3)

    def should_dispatch_command_with_info_id(self):
        bus = RedisCommandBusMother.with_info_id(self.redis_database)
        bus.dispatch(self.command)

        self._assert_command_is_saved_in_bus(bus, self.command)
