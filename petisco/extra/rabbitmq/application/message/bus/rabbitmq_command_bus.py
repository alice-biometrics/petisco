from pika import BasicProperties
from pika.exceptions import ChannelClosedByBroker

from petisco.base.domain.message.command import Command
from petisco.base.domain.message.command_bus import CommandBus
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_configurer import (
    RabbitMqMessageConfigurer,
)
from petisco.extra.rabbitmq.application.message.formatter.rabbitmq_message_queue_name_formatter import (
    RabbitMqMessageQueueNameFormatter,
)
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector


class RabbitMqCommandBus(CommandBus):
    def __init__(
        self,
        organization: str,
        service: str,
        connector: RabbitMqConnector = RabbitMqConnector(),
    ):
        self.connector = connector
        self.exchange_name = f"{organization}.{service}"
        self.rabbitmq_key = f"publisher-{self.exchange_name}"
        self.configurer = RabbitMqMessageConfigurer(organization, service, connector)
        self.properties = BasicProperties(delivery_mode=2)  # PERSISTENT_TEXT_PLAIN

    def dispatch(self, command: Command):
        self._check_is_command(command)
        meta = self.get_configured_meta()
        command = command.update_meta(meta)
        try:
            channel = self.connector.get_channel(self.rabbitmq_key)
            routing_key = RabbitMqMessageQueueNameFormatter.format(
                command, exchange_name=self.exchange_name
            )
            channel.confirm_delivery()
            channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=command.json(),
                properties=self.properties,
            )
        except ChannelClosedByBroker:
            # If domain event queue is not configured, it will be configured and then try to publish again.
            self.configurer.configure()
            self.publish(command)

    def close(self):
        self.connector.close(self.rabbitmq_key)
