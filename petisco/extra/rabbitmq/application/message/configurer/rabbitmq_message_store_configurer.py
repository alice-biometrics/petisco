from petisco.extra.rabbitmq.shared.queue_config import QueueConfig
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector
from petisco.extra.rabbitmq.shared.rabbitmq_declarer import RabbitMqDeclarer
from petisco.extra.rabbitmq.shared.rabbitmq_exchange_name_formatter import (
    RabbitMqExchangeNameFormatter,
)


class RabbitMqMessageStoreConfigurer:
    def __init__(
        self,
        organization: str,
        service: str,
        connector: RabbitMqConnector,
        queue_config: QueueConfig,
    ):
        self._connector = connector
        self._exchange_name = f"{organization}.{service}"
        self._retry_exchange_name = RabbitMqExchangeNameFormatter.retry(
            self._exchange_name
        )
        self._dead_letter_exchange_name = RabbitMqExchangeNameFormatter.dead_letter(
            self._exchange_name
        )
        self._common_retry_exchange_name = f"retry.{organization}.store"
        self._common_dead_letter_exchange_name = f"dead_letter.{organization}.store"

        self.rabbitmq = RabbitMqDeclarer(
            connector=self._connector, channel_name=self._exchange_name
        )
        self.queue_config = queue_config

    def execute(self):
        self._configure_exchanges()
        self._declare_queues(
            self._exchange_name,
            self._retry_exchange_name,
            self._dead_letter_exchange_name,
        )

    def clear(self):
        self._delete_exchange()
        self._delete_queues()

    def _configure_exchanges(self):
        self.rabbitmq.declare_exchange(self._exchange_name)
        self.rabbitmq.declare_exchange(self._retry_exchange_name)
        self.rabbitmq.declare_exchange(self._dead_letter_exchange_name)
        self.rabbitmq.declare_exchange(self._common_retry_exchange_name)
        self.rabbitmq.declare_exchange(self._common_dead_letter_exchange_name)

    def _delete_exchange(self):
        self.rabbitmq.delete_exchange(self._exchange_name)
        self.rabbitmq.delete_exchange(self._retry_exchange_name)
        self.rabbitmq.delete_exchange(self._dead_letter_exchange_name)
        self.rabbitmq.delete_exchange(self._common_retry_exchange_name)
        self.rabbitmq.delete_exchange(self._common_dead_letter_exchange_name)

    def _delete_queues(self):
        self.rabbitmq.delete_queue("store")
        self.rabbitmq.delete_queue("retry.store")
        self.rabbitmq.delete_queue("dead_letter.store")

    def _declare_queues(
        self,
        exchange_name: str,
        retry_exchange_name: str,
        dead_letter_exchange_name: str,
    ):
        self.rabbitmq.declare_queue(
            queue_name="store",
            dead_letter_exchange=self._common_dead_letter_exchange_name,
            dead_letter_routing_key="dead_letter",
            message_ttl=self.queue_config.get_main_ttl("store"),
        )
        self.rabbitmq.declare_queue(
            queue_name="retry.store",
            dead_letter_exchange=self._common_retry_exchange_name,  # exchange_name
            dead_letter_routing_key="store",
            message_ttl=self.queue_config.get_retry_ttl("retry.store"),
        )
        self.rabbitmq.declare_queue(queue_name="dead_letter.store")

        for routing_key_any_message in ["*.*.*.event.*", "*.*.*.command.*"]:
            self.rabbitmq.bind_queue(
                exchange_name=exchange_name,
                queue_name="store",
                routing_key=routing_key_any_message,
            )
            self.rabbitmq.bind_queue(
                exchange_name=self._common_retry_exchange_name,
                queue_name="store",
                routing_key=routing_key_any_message,
            )
            self.rabbitmq.bind_queue(
                exchange_name=dead_letter_exchange_name,
                queue_name="dead_letter.store",
                routing_key=f"dead_letter.{routing_key_any_message}",
            )

        self.rabbitmq.bind_queue(
            exchange_name=exchange_name, queue_name="store", routing_key="retry.store"
        )
        self.rabbitmq.bind_queue(
            exchange_name=exchange_name, queue_name="store", routing_key="store"
        )

        self.rabbitmq.bind_queue(
            exchange_name=self._common_retry_exchange_name,
            queue_name="store",
            routing_key="store",
        )
        self.rabbitmq.bind_queue(
            exchange_name=self._common_retry_exchange_name,
            queue_name="retry.store",
            routing_key="retry.store",
        )
        self.rabbitmq.bind_queue(
            exchange_name=self._common_dead_letter_exchange_name,
            queue_name="dead_letter.store",
            routing_key="dead_letter",
        )
        self.rabbitmq.bind_queue(
            exchange_name=dead_letter_exchange_name,
            queue_name="dead_letter.store",
            routing_key="dead_letter.store",
        )
