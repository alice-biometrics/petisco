from petisco.extra.rabbitmq.is_pika_available import is_pika_available

rabbitmq = []
if is_pika_available():

    from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector
    from petisco.extra.rabbitmq.shared.rabbitmq_declarer import RabbitMqDeclarer
    from petisco.extra.rabbitmq.application.message.bus.rabbitmq_domain_event_bus import (
        RabbitMqDomainEventBus,
    )
    from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_configurer import (
        RabbitMqMessageConfigurer,
    )
    from petisco.extra.rabbitmq.shared.queue_config import QueueConfig
    from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_message_consumer import (
        RabbitMqMessageConsumer,
    )
    from petisco.extra.rabbitmq.application.message.bus.rabbitmq_command_bus import (
        RabbitMqCommandBus,
    )
    from petisco.extra.rabbitmq.dependencies import get_rabbitmq_bus_dependencies
    from petisco.extra.rabbitmq.application.chaos.rabbitmq_message_chaos import (
        RabbitMqMessageChaos,
    )
    from petisco.extra.rabbitmq.shared.specific_queue_config import SpecificQueueConfig

    rabbitmq = [
        "RabbitMqConnector",
        "RabbitMqDeclarer",
        "RabbitMqDomainEventBus",
        "RabbitMqMessageConfigurer",
        "QueueConfig",
        "SpecificQueueConfig",
        "RabbitMqMessageConsumer",
        "RabbitMqCommandBus",
        "get_rabbitmq_bus_dependencies",
        "RabbitMqMessageChaos",
    ]
else:
    from petisco.extra.rabbitmq.dependencies import get_basic_bus_dependencies

    rabbitmq = ["get_basic_bus_dependencies"]

__all__ = rabbitmq
