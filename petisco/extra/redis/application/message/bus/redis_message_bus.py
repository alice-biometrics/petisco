import json
from typing import List, Union

from redis.client import Redis
from redis.exceptions import RedisError

from petisco.base.domain.errors.critical_error import CriticalError
from petisco.base.domain.message.message import Message
from petisco.base.domain.message.message_bus import MessageBus, TypeMessage


class RedisMessageBus(MessageBus):
    """
    A generic implementation of MessageBus using Redis infrastructure.
    """

    def publish(self, message: Union[TypeMessage, List[TypeMessage]]) -> None:
        pass

    def __init__(
        self, organization: str, service: str, redis_database: Redis, database_name: str
    ):
        self.organization = organization
        self.service = service
        self.redis_database = redis_database
        self.database_name = database_name

    def save(self, messages: List[Message]) -> None:
        """
        Save several Message
        """

        updated_messages = []
        for message in messages:
            self._check_is_message(message)
            meta = self.get_configured_meta()
            message = message.update_meta(meta)
            updated_messages.append(message)
        try:
            data = [self._get_formatted_data(message) for message in updated_messages]
            with self.redis_database.pipeline() as pipe:
                pipe.lpush(self.database_name, *data)
                pipe.execute()
        except (TimeoutError, ConnectionError, RedisError) as ex:
            raise CriticalError(additional_info={"error message": str(ex)})

    def _get_formatted_data(self, message: Message):
        formatted_data = {
            "organization": self.organization,
            "service": self.service,
            "message": message.dict(),
        }
        return json.dumps(formatted_data)

    def close(self) -> None:
        pass
