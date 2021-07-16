from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.domain.message.not_implemented_domain_event_bus import (
    NotImplementedDomainEventBusBuilder,
)
from petisco.base.domain.message.not_implemented_message_comsumer import (
    NotImplementedMessageConsumerBuilder,
)
from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_message_consumer import (
    RabbitMqMessageConsumerBuilder,
)


def get_default_message_dependencies() -> List[Dependency]:

    return [
        Dependency(
            name="domain_event_bus",
            default_builder=NotImplementedDomainEventBusBuilder(),
            envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
        ),
        Dependency(
            name="command_bus",
            default_builder=NotImplementedDomainEventBusBuilder(),
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
        ),
        Dependency(
            name="domain_event_consumer",
            default_builder=NotImplementedMessageConsumerBuilder(),
            envar_modifier="PETISCO_DOMAIN_EVENT_CONSUMER_TYPE",
        ),
        Dependency(
            name="command_consumer",
            default_builder=NotImplementedMessageConsumerBuilder(),
            envar_modifier="PETISCO_COMMAND_CONSUMER_TYPE",
        ),
    ]


def get_rabbitmq_message_dependencies(
    organization: str, service: str, max_retries: int = 5
) -> List[Dependency]:
    from petisco.extra.rabbitmq.application.message.bus.rabbitmq_command_bus import (
        RabbitMqCommandBusBuilder,
    )
    from petisco.extra.rabbitmq.application.message.bus.rabbitmq_domain_event_bus import (
        RabbitMqDomainEventBusBuilder,
    )

    return [
        Dependency(
            name="domain_event_bus",
            default_builder=NotImplementedDomainEventBusBuilder(),
            envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
            builders={"rabbitmq": RabbitMqDomainEventBusBuilder(organization, service)},
        ),
        Dependency(
            name="command_bus",
            default_builder=NotImplementedDomainEventBusBuilder(),
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
            builders={"rabbitmq": RabbitMqCommandBusBuilder(organization, service)},
        ),
        Dependency(
            name="domain_event_consumer",
            default_builder=NotImplementedMessageConsumerBuilder(),
            envar_modifier="PETISCO_DOMAIN_EVENT_CONSUMER_TYPE",
            builders={
                "rabbitmq": RabbitMqMessageConsumerBuilder(
                    organization, service, max_retries
                )
            },
        ),
    ]
