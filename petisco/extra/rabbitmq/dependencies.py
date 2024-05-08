from typing import List, Union

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.domain.message.command_bus import CommandBus
from petisco.base.domain.message.domain_event_bus import DomainEventBus
from petisco.base.domain.message.message_configurer import MessageConfigurer
from petisco.base.domain.message.message_consumer import MessageConsumer
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
            DomainEventBus,
            builders={"default": Builder(NotImplementedDomainEventBus)},
            envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
        ),
        Dependency(
            CommandBus,
            builders={"default": Builder(NotImplementedCommandBus)},
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
        ),
        Dependency(
            MessageConfigurer,
            builders={"default": Builder(NotImplementedMessageConfigurer)},
            envar_modifier="PETISCO_MESSAGE_CONFIGURER_TYPE",
        ),
        Dependency(
            MessageConsumer,
            builders={"default": Builder(NotImplementedMessageConsumer)},
            envar_modifier="PETISCO_MESSAGE_CONSUMER_TYPE",
        ),
    ]


def get_rabbitmq_message_dependencies(
    organization: str,
    service: str,
    max_retries: int = 5,
    alias: Union[str, None] = None,
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
            DomainEventBus,
            alias=alias,
            builders={
                "default": Builder(RabbitMqDomainEventBus, organization=organization, service=service),
                "not_implemented": Builder(NotImplementedDomainEventBus),
            },
            envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
        ),
        Dependency(
            CommandBus,
            alias=alias,
            builders={
                "default": Builder(RabbitMqCommandBus, organization=organization, service=service),
                "not_implemented": Builder(NotImplementedCommandBus),
            },
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
        ),
        Dependency(
            MessageConfigurer,
            alias=alias,
            builders={
                "default": Builder(
                    RabbitMqMessageConfigurer,
                    organization=organization,
                    service=service,
                ),
                "not_implemented": Builder(NotImplementedMessageConfigurer),
            },
            envar_modifier="PETISCO_MESSAGE_CONFIGURER_TYPE",
        ),
        Dependency(
            MessageConsumer,
            alias=alias,
            builders={
                "default": Builder(
                    RabbitMqMessageConsumer,
                    organization=organization,
                    service=service,
                    max_retries=max_retries,
                ),
                "not_implemented": Builder(NotImplementedMessageConsumer),
            },
            envar_modifier="PETISCO_MESSAGE_CONSUMER_TYPE",
        ),
    ]
