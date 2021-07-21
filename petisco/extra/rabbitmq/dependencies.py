from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.domain.message.not_implemented_command_bus import (
    NotImplementedCommandBus,
)
from petisco.base.domain.message.not_implemented_domain_event_bus import (
    NotImplementedDomainEventBus,
)
from petisco.base.domain.message.not_implemented_message_comsumer import (
    NotImplementedMessageConsumer,
)
from petisco.base.domain.message.not_implemented_message_configurer import (
    NotImplementedMessageConfigurer,
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
            default_builder=Builder(NotImplementedCommandBus),
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
        ),
        Dependency(
            name="message_configurer",
            default_builder=Builder(NotImplementedMessageConfigurer),
            envar_modifier="PETISCO_MESSAGE_CONFIGURER_TYPE",
        ),
        Dependency(
            name="message_consumer",
            default_builder=Builder(NotImplementedMessageConsumer),
            envar_modifier="PETISCO_MESSAGE_CONSUMER_TYPE",
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
    from petisco.extra.rabbitmq.application.message.configurer.rabbitmq_message_configurer import (
        RabbitMqMessageConfigurer,
    )
    from petisco.extra.rabbitmq.application.message.consumer.rabbitmq_message_consumer import (
        RabbitMqMessageConsumer,
    )

    return [
        Dependency(
            name="domain_event_bus",
            default_builder=Builder(
                RabbitMqDomainEventBus, organization=organization, service=service
            ),
            envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
            builders={"not_implemented": Builder(NotImplementedDomainEventBus)},
        ),
        Dependency(
            name="command_bus",
            default_builder=Builder(
                RabbitMqCommandBus, organization=organization, service=service
            ),
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
            builders={"not_implemented": Builder(NotImplementedCommandBus)},
        ),
        Dependency(
            name="message_configurer",
            default_builder=Builder(
                RabbitMqMessageConfigurer,
                organization=organization,
                service=service,
            ),
            envar_modifier="PETISCO_MESSAGE_CONFIGURER_TYPE",
            builders={"not_implemented": Builder(NotImplementedMessageConfigurer)},
        ),
        Dependency(
            name="message_consumer",
            default_builder=Builder(
                RabbitMqMessageConsumer,
                organization=organization,
                service=service,
                max_retries=max_retries,
            ),
            envar_modifier="PETISCO_MESSAGE_CONSUMER_TYPE",
            builders={"not_implemented": Builder(NotImplementedMessageConsumer)},
        ),
    ]
