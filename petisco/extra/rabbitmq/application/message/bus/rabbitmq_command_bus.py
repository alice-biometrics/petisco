from typing import List, Union

from pika.exceptions import ChannelClosedByBroker

from petisco.base.application.chaos.check_chaos import check_chaos_publication
from petisco.base.domain.message.command import Command
from petisco.base.domain.message.command_bus import CommandBus
from petisco.extra.rabbitmq.application.message.bus.rabbitmq_message_publisher import (
    RabbitMqMessagePublisher,
)
from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_configurer import (
    RabbitMqMessageConfigurer,
)
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_consumer_connector import (
    RabbitMqConsumerConnector,
)
from petisco.extra.rabbitmq.shared.queue_config import QueueConfig
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector


class RabbitMqCommandBus(CommandBus):
    """
    An implementation of CommandBus using RabbitMQ infrastructure.
    Implementation is based on pika library.
    """

    def __init__(
        self,
        organization: str,
        service: str,
        connector: Union[RabbitMqConnector, RabbitMqConsumerConnector] = RabbitMqConnector(),
        fallback: Union[CommandBus, None] = None,
        queue_config: QueueConfig = QueueConfig.default(),
        use_store_queues: bool = True,
    ):
        self.connector = connector
        self.exchange_name = f"{organization}.{service}"
        self.rabbitmq_key = f"publisher-{self.exchange_name}"
        self.configurer = RabbitMqMessageConfigurer(
            organization=organization,
            service=service,
            connector=connector,
            queue_config=queue_config,
            use_store_queues=use_store_queues,
        )
        self.already_configured = False
        self.fallback = fallback
        self.publisher = RabbitMqMessagePublisher(self.exchange_name)

    def dispatch(self, command: Union[Command, List[Command]]) -> None:
        """
        Dispatch one Command or a list of commands

        Dispatch several commands could be a code smell but some use case could require this feature.
        """

        meta = self.get_configured_meta()
        dispatched_commands = []
        commands = self._check_input(command)

        try:
            check_chaos_publication()
            channel = self.connector.get_channel(self.rabbitmq_key)
            for command in commands:
                self._check_is_command(command)
                command = command.update_meta(meta)
                self.publisher.execute(channel, command)
                if channel.is_open and not isinstance(self.connector, RabbitMqConsumerConnector):
                    channel.close()
                dispatched_commands.append(command)
        except ChannelClosedByBroker:
            unpublished_commands = [command for command in commands if command not in dispatched_commands]
            self._retry(unpublished_commands)
        except Exception as exc:  # noqa
            if not self.fallback:
                raise exc

            unpublished_commands = [command for command in commands if command not in dispatched_commands]
            self.fallback.dispatch(unpublished_commands)

    def _retry(self, command: Union[Command, List[Command]]) -> None:
        # If command queue is not configured, it will be configured and then try to dispatch again.
        if not self.already_configured:
            self.configurer.configure()
            self.already_configured = True
            self.dispatch(command)
        elif self.fallback:
            self.fallback.dispatch(command)

    def close(self) -> None:
        """
        Close RabbitMQ connection.
        """
        self.connector.close(self.rabbitmq_key)
