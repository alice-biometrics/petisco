from typing import Any, Dict, Union

from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector


class RabbitMqDeclarer:
    def __init__(self, connector: RabbitMqConnector, channel_name: str):
        self._connector = connector
        self._channel_name = channel_name

    def declare_exchange(self, exchange_name: str, exchange_type: str = "topic") -> None:
        channel = self._connector.get_channel(self._channel_name)
        try:
            channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
        except Exception as error:
            raise TypeError(
                f"RabbitMQEventPublisher: Cannot create the exchange ({exchange_name})\n{error}"
            ) from error
        channel.close()

    def delete_exchange(self, exchange_name: str) -> None:
        channel = self._connector.get_channel(self._channel_name)
        channel.exchange_delete(exchange_name)
        channel.close()

    def declare_queue(
        self,
        queue_name: str,
        dead_letter_exchange: Union[str, None] = None,
        dead_letter_routing_key: Union[str, None] = None,
        message_ttl: Union[int, None] = None,
    ) -> str:
        channel = self._connector.get_channel(self._channel_name)

        queue_arguments: Dict[str, Any] = {}
        if dead_letter_exchange:
            queue_arguments["x-dead-letter-exchange"] = dead_letter_exchange

        if dead_letter_routing_key:
            queue_arguments["x-dead-letter-routing-key"] = dead_letter_routing_key

        if message_ttl:
            queue_arguments["x-message-ttl"] = message_ttl

        result = channel.queue_declare(queue=queue_name, arguments=queue_arguments, durable=True)
        channel.close()

        queue_name: str = result.method.queue

        return queue_name

    def bind_queue(self, exchange_name: str, queue_name: str, routing_key: str) -> None:
        channel = self._connector.get_channel(self._channel_name)

        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
        channel.close()

    def delete_queue(self, queue_name: str) -> None:
        channel = self._connector.get_channel(self._channel_name)
        channel.queue_delete(queue_name)
        channel.close()
