from petisco.extra.rabbitmq.is_pika_available import is_pika_available

rabbitmq = []
if is_pika_available():
    from petisco.extra.rabbitmq.dependencies import (
        get_extra_bus_dependencies as get_available_bus_dependencies,
    )
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

    rabbitmq = [
        "get_available_bus_dependencies",
        "RabbitMqConnector" "RabbitMqDeclarer",
        "RabbitMqDomainEventBus",
        "RabbitMqMessageConfigurer",
        "QueueConfig",
        "RabbitMqMessageConsumer",
    ]
else:
    from petisco.extra.rabbitmq.dependencies import (
        get_basic_bus_dependencies as get_available_bus_dependencies,
    )

    rabbitmq = ["get_available_bus_dependencies"]

__all__ = rabbitmq
