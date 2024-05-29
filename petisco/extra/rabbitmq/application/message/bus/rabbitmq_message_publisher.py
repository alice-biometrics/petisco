from typing import Union

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel

from petisco.base.domain.message.message import Message
from petisco.extra.rabbitmq.application.message.formatter.rabbitmq_message_queue_name_formatter import (
    RabbitMqMessageQueueNameFormatter,
)


class RabbitMqMessagePublisher:
    def __init__(self, exchange_name: str) -> None:
        self._exchange_name = exchange_name
        self._properties = BasicProperties(delivery_mode=2)  # PERSISTENT_TEXT_PLAIN

    def execute(
        self,
        channel: BlockingChannel,
        message: Message,
        routing_key: Union[str, None] = None,
        first_time: bool = False,
    ) -> None:
        if routing_key is None:
            routing_key = RabbitMqMessageQueueNameFormatter.format(message, exchange_name=self._exchange_name)

        if first_time:
            # Confirm delivery should be enabled just once. Source: https://www.rabbitmq.com/tutorials/tutorial-seven-java#enabling-publisher-confirms-on-a-channel
            # Otherwise with Pika we get lots of error messages
            channel.confirm_delivery()
        channel.basic_publish(
            exchange=self._exchange_name,
            routing_key=routing_key,
            body=message.format_json().encode(),
            properties=self._properties,
        )
