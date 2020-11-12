from petisco.logger.interface_logger import ILogger
from petisco.event.shared.domain.config_events import ConfigEvents
from petisco.event.bus.infrastructure.not_implemented_event_bus import (
    NotImplementedEventBus,
)
from petisco.event.configurer.infrastructure.not_implemented_configurer import (
    NotImplementedEventConfigurer,
)
from petisco.event.consumer.infrastructure.not_implemented_event_comsumer import (
    NotImplementedEventConsumer,
)


def configure_events_infrastructure(config_events: ConfigEvents, logger: ILogger):
    bus = NotImplementedEventBus()
    configurer = NotImplementedEventConfigurer()
    consumer = NotImplementedEventConsumer()

    if config_events.message_broker == "rabbitmq":
        from petisco.event.shared.infrastructure.rabbitmq.rabbitmq_connector import (
            RabbitMqConnector,
        )
        from petisco.event.bus.infrastructure.rabbitmq_event_bus import RabbitMqEventBus
        from petisco.event.configurer.infrastructure.rabbitmq_event_configurer import (
            RabbitMqEventConfigurer,
        )
        from petisco.event.consumer.infrastructure.rabbitmq_event_consumer import (
            RabbitMqEventConsumer,
        )

        bus = RabbitMqEventBus(
            connector=RabbitMqConnector(),
            organization=config_events.organization,
            service=config_events.service,
        )
        configurer = RabbitMqEventConfigurer(
            connector=RabbitMqConnector(),
            organization=config_events.organization,
            service=config_events.service,
            use_store_queues=config_events.use_store_queues,
            queue_config=config_events.queue_config,
        )

        consumer = RabbitMqEventConsumer(
            connector=RabbitMqConnector(),
            organization=config_events.organization,
            service=config_events.service,
            max_retries=config_events.max_retries,
            verbose=config_events.consumer_verbose,
            logger=logger,
            chaos=config_events.chaos,
        )

    return bus, configurer, consumer
