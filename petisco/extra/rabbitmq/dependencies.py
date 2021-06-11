from typing import List

from petisco.base.application.dependency_injection.dependency import Dependency
from petisco.base.domain.message.not_implemented_domain_event_bus import (
    NotImplementedDomainEventBus,
)
from petisco.extra.rabbitmq.application.message.rabbitmq_domain_event_bus import (
    RabbitMqDomainEventBus,
)
from petisco.extra.rabbitmq.shared.rabbitmq_connector import RabbitMqConnector


def get_basic_bus_dependencies(
    organization: str = None, service: str = None
) -> List[Dependency]:

    return [
        Dependency(
            name="domain_event_bus",
            default_instance=NotImplementedDomainEventBus(),
            envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
        ),
        Dependency(
            name="command_bus",
            default_instance=NotImplementedDomainEventBus(),
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
        ),
    ]


def get_extra_bus_dependencies(organization: str, service: str) -> List[Dependency]:

    return [
        Dependency(
            name="domain_event_bus",
            default_instance=NotImplementedDomainEventBus(),
            envar_modifier="PETISCO_DOMAIN_EVENT_BUS_TYPE",
            instances={
                "rabbitmq": RabbitMqDomainEventBus(
                    connector=RabbitMqConnector(),
                    organization=organization,
                    service=service,
                )
            },
        ),
        Dependency(
            name="command_bus",
            default_instance=NotImplementedDomainEventBus(),
            envar_modifier="PETISCO_COMMAND_BUS_TYPE",
            instances={
                "rabbitmq": RabbitMqDomainEventBus(
                    connector=RabbitMqConnector(),
                    organization=organization,
                    service=service,
                )
            },
        ),
    ]
