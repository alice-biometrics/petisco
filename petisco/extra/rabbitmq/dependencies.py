from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.domain.message.not_implemented_domain_event_bus import (
    NotImplementedDomainEventBus,
)
from petisco.base.domain.message.not_implemented_message_comsumer import (
    NotImplementedMessageConsumer,
)
from petisco.base.misc.builder import Builder


def get_default_message_dependencies() -> List[Dependency]:

    return [
        Dependency(
            name="domain_event_bus",
            default_builder=Builder(NotImplementedDomainEventBus),
            envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
        ),
        Dependency(
            name="command_bus",
            default_builder=Builder(NotImplementedDomainEventBus),
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
        ),
        Dependency(
            name="domain_event_consumer",
            default_builder=Builder(NotImplementedMessageConsumer),
            envar_modifier="PETISCO_DOMAIN_EVENT_CONSUMER_TYPE",
        ),
        Dependency(
            name="command_consumer",
            default_builder=Builder(NotImplementedMessageConsumer),
            envar_modifier="PETISCO_COMMAND_CONSUMER_TYPE",
        ),
    ]


def get_rabbitmq_message_dependencies(
    organization: str, service: str, max_retries: int = 5
) -> List[Dependency]:
    from petisco.extra.rabbitmq.application.message.bus.rabbitmq_command_bus import (
        RabbitMqCommandBus,
    )
    from petisco.extra.rabbitmq.application.message.bus.rabbitmq_domain_event_bus import (
        RabbitMqDomainEventBus,
    )
    from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_message_consumer import (
        RabbitMqMessageConsumer,
    )

    return [
        Dependency(
            name="domain_event_bus",
            default_builder=Builder(NotImplementedDomainEventBus),
            envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
            builders={
                "rabbitmq": Builder(RabbitMqDomainEventBus, organization, service)
            },
        ),
        Dependency(
            name="command_bus",
            default_builder=Builder(NotImplementedDomainEventBus),
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
            builders={"rabbitmq": Builder(RabbitMqCommandBus, organization, service)},
        ),
        Dependency(
            name="domain_event_consumer",
            default_builder=Builder(NotImplementedMessageConsumer),
            envar_modifier="PETISCO_DOMAIN_EVENT_CONSUMER_TYPE",
            builders={
                "rabbitmq": Builder(
                    RabbitMqMessageConsumer, organization, service, max_retries
                )
            },
        ),
    ]
